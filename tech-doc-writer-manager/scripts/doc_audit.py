#!/usr/bin/env python3
"""
Documentation Auditor

Analyzes documentation health and identifies issues:
- Stale documents (not updated recently)
- Missing metadata fields
- Broken cross-references
- Status distribution
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


REQUIRED_METADATA = ["title", "doc_type", "status", "created", "last_updated"]
VALID_STATUSES = ["draft", "review", "published", "deprecated"]
VALID_DOC_TYPES = ["api", "integration", "testing", "architecture", "runbook", "guide"]


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}
    
    frontmatter = {}
    for line in match.group(1).strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            if value.startswith('['):
                try:
                    value = json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    value = []
            frontmatter[key] = value
    return frontmatter


def extract_links(content: str) -> list:
    """Extract all markdown links from content."""
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return [(text, url) for text, url in re.findall(pattern, content)]


def audit_document(doc_path: Path, project_path: Path, stale_days: int = 90) -> dict:
    """Audit a single document for issues."""
    issues = []
    warnings = []
    
    try:
        content = doc_path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "path": str(doc_path.relative_to(project_path)),
            "status": "error",
            "issues": [f"Cannot read file: {e}"],
            "warnings": []
        }
    
    meta = parse_frontmatter(content)
    rel_path = str(doc_path.relative_to(project_path))
    
    # Check for missing metadata
    missing_fields = [f for f in REQUIRED_METADATA if f not in meta]
    if missing_fields:
        issues.append(f"Missing required metadata: {', '.join(missing_fields)}")
    
    # Validate metadata values
    if meta.get("status") and meta["status"] not in VALID_STATUSES:
        warnings.append(f"Invalid status '{meta['status']}', expected one of: {VALID_STATUSES}")
    
    if meta.get("doc_type") and meta["doc_type"] not in VALID_DOC_TYPES:
        warnings.append(f"Invalid doc_type '{meta['doc_type']}', expected one of: {VALID_DOC_TYPES}")
    
    # Check staleness
    staleness = -1
    if "last_updated" in meta:
        try:
            updated = datetime.strptime(meta["last_updated"], "%Y-%m-%d")
            staleness = (datetime.now() - updated).days
            if staleness > stale_days:
                warnings.append(f"Document is stale ({staleness} days since last update)")
        except ValueError:
            issues.append(f"Invalid date format for last_updated: {meta['last_updated']}")
    
    # Check for broken internal links
    links = extract_links(content)
    docs_dir = project_path / "docs"
    for link_text, link_url in links:
        if link_url.startswith(("http://", "https://", "#")):
            continue
        linked_path = (doc_path.parent / link_url).resolve()
        if not linked_path.exists():
            issues.append(f"Broken link: [{link_text}]({link_url})")
    
    # Check content quality
    word_count = len(content.split())
    if word_count < 50:
        warnings.append(f"Document is very short ({word_count} words)")
    
    # Determine overall status
    if issues:
        status = "fail"
    elif warnings:
        status = "warn"
    else:
        status = "pass"
    
    return {
        "path": rel_path,
        "title": meta.get("title", doc_path.stem),
        "doc_type": meta.get("doc_type", "unknown"),
        "doc_status": meta.get("status", "unknown"),
        "staleness_days": staleness,
        "word_count": word_count,
        "audit_status": status,
        "issues": issues,
        "warnings": warnings
    }


def audit_project(project_path: Path, stale_days: int = 90) -> dict:
    """Audit all documentation in a project."""
    docs_dir = project_path / "docs"
    
    if not docs_dir.exists():
        return {
            "project": project_path.name,
            "timestamp": datetime.now().isoformat(),
            "error": "No docs/ directory found",
            "documents": []
        }
    
    results = []
    for md_file in docs_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
        results.append(audit_document(md_file, project_path, stale_days))
    
    # Calculate summary
    total = len(results)
    passed = sum(1 for r in results if r["audit_status"] == "pass")
    warned = sum(1 for r in results if r["audit_status"] == "warn")
    failed = sum(1 for r in results if r["audit_status"] == "fail")
    stale = sum(1 for r in results if r.get("staleness_days", 0) > stale_days)
    
    # Get issues requiring attention
    attention_needed = [
        {
            "path": r["path"],
            "title": r.get("title", "Unknown"),
            "issues": r["issues"],
            "warnings": r["warnings"]
        }
        for r in results if r["audit_status"] in ("fail", "warn")
    ]
    
    return {
        "project": project_path.name,
        "timestamp": datetime.now().isoformat(),
        "stale_threshold_days": stale_days,
        "summary": {
            "total_documents": total,
            "passed": passed,
            "warnings": warned,
            "failed": failed,
            "stale_documents": stale,
            "health_score": round((passed / total * 100) if total > 0 else 0, 1)
        },
        "attention_needed": attention_needed,
        "all_documents": results
    }


def format_report(audit_result: dict, output_format: str) -> str:
    """Format audit results for output."""
    if output_format == "json":
        return json.dumps(audit_result, indent=2)
    
    # Markdown format
    lines = [
        f"# Documentation Audit Report",
        f"",
        f"**Project**: {audit_result['project']}",
        f"**Date**: {audit_result['timestamp']}",
        f"**Stale Threshold**: {audit_result['stale_threshold_days']} days",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Documents | {audit_result['summary']['total_documents']} |",
        f"| Passed | {audit_result['summary']['passed']} |",
        f"| Warnings | {audit_result['summary']['warnings']} |",
        f"| Failed | {audit_result['summary']['failed']} |",
        f"| Stale Documents | {audit_result['summary']['stale_documents']} |",
        f"| Health Score | {audit_result['summary']['health_score']}% |",
        f"",
    ]
    
    if audit_result["attention_needed"]:
        lines.extend([
            f"## Documents Needing Attention",
            f"",
        ])
        for doc in audit_result["attention_needed"]:
            lines.append(f"### {doc['title']}")
            lines.append(f"**Path**: `{doc['path']}`")
            if doc["issues"]:
                lines.append(f"**Issues**:")
                for issue in doc["issues"]:
                    lines.append(f"- {issue}")
            if doc["warnings"]:
                lines.append(f"**Warnings**:")
                for warning in doc["warnings"]:
                    lines.append(f"- {warning}")
            lines.append("")
    else:
        lines.extend([
            f"## Status",
            f"",
            f"All documents passed audit checks.",
            f"",
        ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit documentation health")
    parser.add_argument("--project-path", type=Path, required=True)
    parser.add_argument("--stale-days", type=int, default=90, help="Days before doc is considered stale")
    parser.add_argument("--output", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    
    project_path = args.project_path.resolve()
    result = audit_project(project_path, args.stale_days)
    print(format_report(result, args.output))


if __name__ == "__main__":
    main()
