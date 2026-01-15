#!/usr/bin/env python3
"""
Documentation Index Manager

Manages the docs/_index.json file for documentation inventory tracking.
Supports rebuilding, adding, removing, and querying document entries.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


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


def calculate_staleness(last_updated: str) -> int:
    """Calculate days since last update."""
    try:
        updated = datetime.strptime(last_updated, "%Y-%m-%d")
        return (datetime.now() - updated).days
    except (ValueError, TypeError):
        return -1


def create_doc_entry(doc_path: Path, project_path: Path) -> dict:
    """Create an index entry from a document file."""
    content = doc_path.read_text(encoding='utf-8')
    meta = parse_frontmatter(content)
    rel_path = str(doc_path.relative_to(project_path))
    
    return {
        "title": meta.get("title", doc_path.stem.replace("-", " ").title()),
        "path": rel_path,
        "doc_type": meta.get("doc_type", "guide"),
        "status": meta.get("status", "draft"),
        "version": meta.get("version", "1.0.0"),
        "created": meta.get("created", datetime.now().strftime("%Y-%m-%d")),
        "last_updated": meta.get("last_updated", datetime.now().strftime("%Y-%m-%d")),
        "staleness_days": calculate_staleness(meta.get("last_updated")),
        "tags": meta.get("tags", []),
        "related_docs": meta.get("related_docs", [])
    }


def calculate_summary(documents: list) -> dict:
    """Calculate summary statistics from document list."""
    summary = {
        "total": len(documents),
        "by_status": {"published": 0, "draft": 0, "review": 0, "deprecated": 0},
        "by_type": {"api": 0, "integration": 0, "testing": 0, "architecture": 0, "runbook": 0, "guide": 0}
    }
    
    for doc in documents:
        status = doc.get("status", "draft")
        doc_type = doc.get("doc_type", "guide")
        if status in summary["by_status"]:
            summary["by_status"][status] += 1
        if doc_type in summary["by_type"]:
            summary["by_type"][doc_type] += 1
    
    return summary


def rebuild_index(project_path: Path) -> dict:
    """Rebuild the entire index from scratch."""
    docs_dir = project_path / "docs"
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True)
    
    documents = []
    for md_file in docs_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
        documents.append(create_doc_entry(md_file, project_path))
    
    index = {
        "project": project_path.name,
        "last_audit": datetime.now(timezone.utc).isoformat(),
        "summary": calculate_summary(documents),
        "documents": sorted(documents, key=lambda x: x["path"])
    }
    
    return index


def add_document(index: dict, doc_path: Path, project_path: Path) -> dict:
    """Add or update a document in the index."""
    entry = create_doc_entry(doc_path, project_path)
    rel_path = str(doc_path.relative_to(project_path))
    
    # Remove existing entry if present
    index["documents"] = [d for d in index["documents"] if d["path"] != rel_path]
    index["documents"].append(entry)
    index["documents"] = sorted(index["documents"], key=lambda x: x["path"])
    index["summary"] = calculate_summary(index["documents"])
    index["last_audit"] = datetime.now(timezone.utc).isoformat()
    
    return index


def remove_document(index: dict, doc_path: str) -> dict:
    """Remove a document from the index."""
    index["documents"] = [d for d in index["documents"] if d["path"] != doc_path]
    index["summary"] = calculate_summary(index["documents"])
    index["last_audit"] = datetime.now(timezone.utc).isoformat()
    return index


def load_index(project_path: Path) -> dict:
    """Load existing index or create empty one."""
    index_path = project_path / "docs" / "_index.json"
    if index_path.exists():
        return json.loads(index_path.read_text(encoding='utf-8'))
    return {
        "project": project_path.name,
        "last_audit": None,
        "summary": calculate_summary([]),
        "documents": []
    }


def save_index(index: dict, project_path: Path) -> None:
    """Save index to file."""
    index_path = project_path / "docs" / "_index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description="Manage documentation index")
    parser.add_argument("command", choices=["rebuild", "add", "remove", "show"])
    parser.add_argument("--project-path", type=Path, required=True)
    parser.add_argument("--doc-path", type=Path, help="Path to document (for add/remove)")
    args = parser.parse_args()
    
    project_path = args.project_path.resolve()
    
    if args.command == "rebuild":
        index = rebuild_index(project_path)
        save_index(index, project_path)
        print(json.dumps({"action": "rebuild", "total_docs": index["summary"]["total"]}, indent=2))
    
    elif args.command == "add":
        if not args.doc_path:
            print("Error: --doc-path required for add command", file=sys.stderr)
            sys.exit(1)
        index = load_index(project_path)
        index = add_document(index, args.doc_path.resolve(), project_path)
        save_index(index, project_path)
        print(json.dumps({"action": "add", "path": str(args.doc_path)}, indent=2))
    
    elif args.command == "remove":
        if not args.doc_path:
            print("Error: --doc-path required for remove command", file=sys.stderr)
            sys.exit(1)
        index = load_index(project_path)
        index = remove_document(index, str(args.doc_path))
        save_index(index, project_path)
        print(json.dumps({"action": "remove", "path": str(args.doc_path)}, indent=2))
    
    elif args.command == "show":
        index = load_index(project_path)
        print(json.dumps(index, indent=2))


if __name__ == "__main__":
    main()
