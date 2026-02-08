# Confirmation Format Standard

All confirmations in the framework use a strict command-line style format.

## y/n Confirmations

**Format:** Single line ending with `(y/n)`

**Valid responses (exactly one character):**
- `y` or `Y` → Yes / Proceed
- `n` or `N` → No / Cancel

**Invalid responses:**
- `yes`, `no` → rejected (more than one char)
- `y, sure`, `n thanks` → rejected (more than one char)
- `Y!`, ` y` → rejected (extra characters or whitespace)
- `1`, `0`, `ok` → rejected (not y/n)

**On invalid response:** Re-prompt with the exact same line. No explanation.

---

## Examples by Context

### Collab Mode: Role Confirmation

When user invokes role(s), confirm before proceeding:

```
🤝 Invoking [TPO]. (y/n)
```

Multiple roles:
```
🤝 Invoking [TPO, SA]. (y/n)
```

### Explore Mode: Topic Documentation

When topic changes, ask to document previous topic:

```
🔍 Document [Redis caching] findings? (y/n)
```

At exit:
```
🔍 Document current topic? (y/n)
```

### Explore Mode: Follow-up Ticket

After documenting, optionally create ticket:

```
🔍 Create follow-up ticket? (y/n)
```

---

## Why This Format

1. **Speed** — Single character response is fast
2. **Explicit** — No ambiguity about what user intended
3. **Command-line familiar** — Developers expect this pattern
4. **Prevents mistakes** — Can't accidentally confirm with trailing text

---

## Implementation Notes

When implementing y/n confirmation in any skill:

1. Prompt must end with `(y/n)`
2. Check response is exactly 1 character
3. Check character is `y`, `Y`, `n`, or `N`
4. If invalid, repeat exact same prompt (no error message)
5. Do not proceed until valid response received
