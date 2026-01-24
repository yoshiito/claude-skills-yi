#!/usr/bin/env python3
"""
Generate SKILL.md from skill.yaml

Usage:
    python generate-skill.py <skill-directory>
    python generate-skill.py --all                 # Generate all skills
    python generate-skill.py --validate <skill>    # Validate without generating
    python generate-skill.py --diff <skill>        # Show diff between yaml and existing md

Examples:
    python generate-skill.py backend-fastapi-postgres-sqlmodel-developer
    python generate-skill.py ../program-manager
    python generate-skill.py --all
"""

import sys
import yaml
import argparse
from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader, TemplateError


# =============================================================================
# CONFIGURATION
# =============================================================================

SKILLS_ROOT = Path(__file__).parent.parent.parent  # skills/
TEMPLATE_DIR = Path(__file__).parent  # skill-creator/references/
TEMPLATE_NAME = "skill-template.md.j2"

# Skills that should NOT be generated (meta skills, manual maintenance)
EXCLUDED_SKILLS = ["skill-creator"]


# =============================================================================
# SCHEMA VALIDATION
# =============================================================================

REQUIRED_FIELDS = {
    "meta": ["name", "displayName", "emoji", "description"],
    "role": ["prefix", "capabilities"],
    "role.capabilities": [
        "canIntakeUserRequests",
        "requiresActivationConfirmation",
        "requiresProjectScope",
        "isUtility",
    ],
    "boundaries": ["authorizedActions", "prohibitions"],
    "workflow": ["phases"],
    "references": [],  # Can be empty but must exist
    "relatedSkills": [],  # Can be empty but must exist
}


def validate_schema(data: dict, skill_name: str) -> list[str]:
    """Validate skill.yaml against required schema. Returns list of errors."""
    errors = []

    for section, fields in REQUIRED_FIELDS.items():
        if "." in section:
            # Nested field like "role.capabilities"
            parts = section.split(".")
            current = data
            for part in parts:
                current = current.get(part, {})
            section_data = current
        else:
            section_data = data.get(section)

        if section_data is None:
            errors.append(f"Missing required section: {section}")
            continue

        for field in fields:
            if field not in section_data:
                errors.append(f"Missing required field: {section}.{field}")

    # Validate boundaries have content
    if "boundaries" in data:
        if not data["boundaries"].get("authorizedActions"):
            errors.append("boundaries.authorizedActions cannot be empty")
        if not data["boundaries"].get("prohibitions"):
            errors.append("boundaries.prohibitions cannot be empty")

    # Validate workflow has at least one phase
    if "workflow" in data:
        if not data["workflow"].get("phases"):
            errors.append("workflow.phases cannot be empty")

    return errors


# =============================================================================
# GENERATION
# =============================================================================


def load_yaml(yaml_path: Path) -> dict:
    """Load and parse skill.yaml file."""
    with open(yaml_path) as f:
        return yaml.safe_load(f)


def generate_skill_md(data: dict, template_env: Environment) -> str:
    """Generate SKILL.md content from yaml data."""
    template = template_env.get_template(TEMPLATE_NAME)
    return template.render(**data)


def process_skill(
    skill_dir: Path,
    template_env: Environment,
    validate_only: bool = False,
    show_diff: bool = False,
) -> bool:
    """Process a single skill directory. Returns True if successful."""
    yaml_path = skill_dir / "skill.yaml"
    output_path = skill_dir / "SKILL.md"

    if not yaml_path.exists():
        print(f"  ⚠️  No skill.yaml found in {skill_dir.name}")
        return False

    # Load yaml
    try:
        data = load_yaml(yaml_path)
    except yaml.YAMLError as e:
        print(f"  ❌ YAML parse error: {e}")
        return False

    # Validate
    errors = validate_schema(data, skill_dir.name)
    if errors:
        print(f"  ❌ Validation errors:")
        for error in errors:
            print(f"     - {error}")
        return False

    if validate_only:
        print(f"  ✅ Valid")
        return True

    # Generate
    try:
        content = generate_skill_md(data, template_env)
    except TemplateError as e:
        print(f"  ❌ Template error: {e}")
        return False

    if show_diff:
        if output_path.exists():
            existing = output_path.read_text()
            if existing == content:
                print(f"  ✅ No changes")
            else:
                print(f"  📝 Changes detected (diff not implemented yet)")
        else:
            print(f"  📝 New file would be created")
        return True

    # Write output
    output_path.write_text(content)
    print(f"  ✅ Generated {output_path.name}")
    return True


# =============================================================================
# CLI
# =============================================================================


def find_all_skills() -> list[Path]:
    """Find all skill directories (those with SKILL.md or skill.yaml)."""
    skills = []
    for item in SKILLS_ROOT.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith("_"):
            continue
        if item.name in EXCLUDED_SKILLS:
            continue
        if (item / "skill.yaml").exists() or (item / "SKILL.md").exists():
            skills.append(item)
    return sorted(skills)


def main():
    parser = argparse.ArgumentParser(description="Generate SKILL.md from skill.yaml")
    parser.add_argument("skill", nargs="?", help="Skill directory name or path")
    parser.add_argument("--all", action="store_true", help="Process all skills")
    parser.add_argument(
        "--validate", action="store_true", help="Validate without generating"
    )
    parser.add_argument(
        "--diff", action="store_true", help="Show diff without writing"
    )
    parser.add_argument("--list", action="store_true", help="List all skills")

    args = parser.parse_args()

    # Setup template environment
    template_env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    if args.list:
        print("Skills found:")
        for skill in find_all_skills():
            has_yaml = (skill / "skill.yaml").exists()
            has_md = (skill / "SKILL.md").exists()
            status = "✅" if has_yaml else "📝"
            print(f"  {status} {skill.name}")
        return

    if args.all:
        skills = find_all_skills()
        print(f"Processing {len(skills)} skills...\n")

        success = 0
        failed = 0

        for skill_dir in skills:
            print(f"[{skill_dir.name}]")
            if process_skill(skill_dir, template_env, args.validate, args.diff):
                success += 1
            else:
                failed += 1

        print(f"\nSummary: {success} succeeded, {failed} failed")
        sys.exit(0 if failed == 0 else 1)

    if not args.skill:
        parser.print_help()
        sys.exit(1)

    # Single skill
    skill_path = Path(args.skill)
    if not skill_path.is_absolute():
        # Try relative to skills root
        skill_path = SKILLS_ROOT / args.skill

    if not skill_path.exists():
        print(f"Error: Skill directory not found: {skill_path}")
        sys.exit(1)

    print(f"[{skill_path.name}]")
    success = process_skill(skill_path, template_env, args.validate, args.diff)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
