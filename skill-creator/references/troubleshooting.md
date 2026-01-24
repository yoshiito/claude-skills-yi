# Skill Troubleshooting Guide

## Diagnosis: What to Edit

| Problem | Edit This |
|---------|-----------|
| Format wrong (section order, preamble style) | `skill-template.md.j2` |
| Data wrong (boundaries, workflow) | `skill.yaml` → regenerate |
| Custom content wrong (tech stack, unique sections) | `customSections` in `skill.yaml` |
| Generation error | Check YAML syntax, then template |

## Common Errors

| Error | Fix |
|-------|-----|
| `Missing required section: X` | Add field to skill.yaml |
| `Template error: 'X' has no attribute 'Y'` | Check example YAMLs for structure |
| `YAML parse error` | Fix indentation/quotes |
| Frontmatter not hidden in preview | Remove any content before `---` |
| Wrong role type in preamble | Check `canIntakeUserRequests`, `isUtility` in capabilities |

## Validation Commands

```bash
python generate-skill.py --validate {skill}  # Check without generating
python generate-skill.py --diff {skill}      # Preview changes
python generate-skill.py --all               # Regenerate all
```

## Files Reference

| File | Edit When |
|------|-----------|
| `skill.yaml` | Content changes for ONE skill |
| `skill-template.md.j2` | Format changes for ALL skills |
| `skill-schema.md` | Adding new schema elements |
