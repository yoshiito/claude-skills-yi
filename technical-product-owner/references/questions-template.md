# Questions Template

Track open questions during discovery phase. **All questions must be resolved before creating MRD.**

```markdown
# Questions: [Feature Name]

**Status**: [Open | All Resolved]
**Last Updated**: [date]

## Open Questions

### Q1: [Question text]
- **Area**: [Problem | Users | Success | Scope | Priority | Technical | Other]
- **Asked**: [date]
- **Blocking**: [What this blocks - e.g., "MRD Section 2"]
- **Status**: Open

### Q2: [Question text]
- **Area**: [area]
- **Asked**: [date]
- **Blocking**: [what]
- **Status**: Open

---

## Resolved Questions

### Q3: [Question text]
- **Area**: [area]
- **Asked**: [date]
- **Resolved**: [date]
- **Answer**: [The answer received]
- **Decided By**: [who made the decision]

---

## Question Categories

Use these areas to categorize questions:

| Area | Examples |
|------|----------|
| Problem | Is this validated? What's the cost of not solving? |
| Users | Who specifically? What are their goals? |
| Success | How do we measure? What's the target? |
| Scope | What's out? Why these boundaries? |
| Priority | Why now? What's the urgency? |
| Technical | Constraints that affect requirements (NOT solutions) |
| Other | Stakeholder, budget, legal, etc. |
```

## Usage

1. Create `questions.md` when starting discovery for a new feature
2. Add questions as they arise during conversations
3. Mark questions as resolved with answers when received
4. Only proceed to MRD when Status is "All Resolved"
5. Keep file for historical record even after MRD is complete
