# Naming Conventions Standard

**Guiding Principle**: snake_case is the default for all data contracts (APIs, MCP, database). Language-specific code follows its ecosystem conventions.

---

## Language-Specific Conventions (Code)

| Language | Variables | Functions | Classes | Constants |
|----------|-----------|-----------|---------|-----------|
| **Python** | snake_case | snake_case | PascalCase | SCREAMING_SNAKE_CASE |
| **JavaScript/TS** | camelCase | camelCase | PascalCase | SCREAMING_SNAKE_CASE |
| **Java/Kotlin/C#** | camelCase | camelCase | PascalCase | SCREAMING_SNAKE_CASE |
| **Go (exported)** | PascalCase | PascalCase | PascalCase | PascalCase |
| **Go (unexported)** | camelCase | camelCase | - | camelCase |
| **Rust** | snake_case | snake_case | PascalCase | SCREAMING_SNAKE_CASE |
| **Ruby** | snake_case | snake_case | PascalCase | SCREAMING_SNAKE_CASE |

---

## Contract Conventions (Data Boundaries)

| Context | Convention | Examples |
|---------|------------|----------|
| **REST API** | snake_case | `user_id`, `created_at`, `order_items` |
| **MCP Tools** | snake_case | `get_user_by_id`, `execute_code` |
| **MCP Parameters** | snake_case | `file_path`, `user_id`, `include_metadata` |
| **Database Tables** | snake_case, plural | `users`, `order_items` |
| **Database Columns** | snake_case | `user_email`, `created_at` |
| **JSON Keys** | snake_case | `{"user_name": "...", "is_active": true}` |

---

## Universal Rules (All Contexts)

| Element | Convention | Examples |
|---------|------------|----------|
| **Constants** | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_TIMEOUT` |
| **Classes/Types** | PascalCase | `UserService`, `OrderRepository` |
| **Booleans** | Prefixed question | `is_valid`, `has_permission`, `can_edit` |

---

## Boundary Behavior

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (JS/TS)                                       │
│  camelCase internally                                   │
│                                                         │
│  Transform at API boundary: snake ↔ camel               │
└─────────────────────────┬───────────────────────────────┘
                          │ snake_case
                          ▼
┌─────────────────────────────────────────────────────────┐
│  REST API (FastAPI)                                     │
│  snake_case in/out                                      │
└─────────────────────────┬───────────────────────────────┘
                          │ snake_case
                          ▼
┌─────────────────────────────────────────────────────────┐
│  MCP Tools                                              │
│  snake_case names and parameters                        │
└─────────────────────────┬───────────────────────────────┘
                          │ snake_case
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Database                                               │
│  snake_case tables and columns                          │
└─────────────────────────────────────────────────────────┘
```

---

## Summary

> **"snake_case everywhere except inside JS/TS code."**

Frontend does its own thing internally, but the moment data crosses a boundary (API call, MCP tool, database query), it's snake_case.

---

## Review Guidance

When reviewing code for naming conventions:

1. **Contract check**: Are API/MCP/DB names snake_case?
2. **Language check**: Does code follow language conventions?
3. **Boundary check**: Is transformation happening at the right layer?
4. **Consistency check**: Is it consistent within the file/module?

**Severity**:
- Wrong convention at data boundary (API/MCP/DB): **High**
- Wrong case convention for language: **Medium**
- Inconsistent within file: **Medium**
