# Progress Comment Formats

Workers add structured comments at workflow phase transitions. These formats ensure consistent communication and traceability.

## When Starting Development

```markdown
🚀 **Development Started**
- Feature Branch: `{branch-name}` (confirmed with user)
- Approach: [Brief implementation approach]
```

## When PR Created (Development Complete)

```markdown
🔍 **Ready for Code Review**
- PR: [link] (targeting {feature-branch})
- Changes: [Brief summary]
- Dev subtasks: [All complete / N/A]
```

## When Code Review Complete

```markdown
✅ **Code Review Complete**
- PR: [link]
- Status: Approved and merged
- Ready for: Testing
```

## When Test Complete

```markdown
✅ **Test Complete**
- Tests: [X] unit, [Y] functional
- Coverage: [Z]%
- All passing: ✅
- Ready for: Documentation
```

## When SA Review Complete

```markdown
✅ **SA Review Complete**
- Architecture compliance: ✅
- ADR requirements: Met
- Query integration: [N/A / Verified]
- Ready for: UAT
```

## When UAT Complete (Feature Done)

```markdown
✅ **UAT Complete - Feature Done**
- Acceptance criteria: All met
- User flows: ✅ Working as expected
- Feature ready to close
```
