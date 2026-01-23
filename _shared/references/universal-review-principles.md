# Universal Code Review Principles

Language-agnostic, stack-agnostic principles that apply to ALL code reviews.

These principles complement stack-specific standards enforced by active worker skills.

---

## Security Principles (CRITICAL)

### Principle 1: No Secrets in Code
**What to check**: API keys, passwords, tokens, connection strings, private keys
**Applies to**: All languages, all files
**Severity**: Critical

### Principle 2: Validate External Input
**What to check**: User input, API parameters, file uploads, query strings
**Look for**: Type validation, range checks, format validation, sanitization
**Applies to**: All languages, all entry points
**Severity**: Critical

### Principle 3: Prevent Injection Attacks
**What to check**: SQL, command injection, XSS, path traversal
**Look for**: Parameterized queries, proper escaping, output encoding
**Applies to**: Databases, shells, templates, file systems
**Severity**: Critical

### Principle 4: Authentication & Authorization
**What to check**: Protected endpoints verify user identity and permissions
**Look for**: Auth middleware, permission checks, session validation
**Applies to**: All API endpoints, protected resources
**Severity**: Critical

### Principle 5: No Sensitive Data Leakage
**What to check**: Logs, error messages, API responses
**Look for**: Passwords, tokens, PII, stack traces in user-facing errors
**Applies to**: Logging, error handling, API responses
**Severity**: Critical

---

## Error Handling Principles

### Principle 6: Explicit Error Handling
**What to check**: Try/catch blocks, error returns, null checks
**Look for**: Specific exception types, not generic catch-all
**Applies to**: All languages
**Severity**: High

### Principle 7: No Silent Failures
**What to check**: Empty catch blocks, ignored errors
**Look for**: Proper logging and handling or re-raising
**Applies to**: All error scenarios
**Severity**: High

### Principle 8: Safe Error Messages
**What to check**: User-facing error messages
**Look for**: Generic messages to users, detailed logs internally
**Applies to**: API responses, UI messages
**Severity**: Medium

---

## Code Quality Principles

### Principle 9: Self-Documenting Names
**What to check**: Variables, functions, classes, files
**Look for**: Descriptive names that explain intent
**Applies to**: All identifiers
**Severity**: Medium

### Principle 10: Single Responsibility
**What to check**: Functions/methods length and complexity
**Look for**: Functions doing one thing well
**Applies to**: All functions, classes, modules
**Severity**: Medium

### Principle 11: No Dead Code
**What to check**: Commented-out code, unused variables, unreachable code
**Look for**: Clean, active code only
**Applies to**: All files
**Severity**: Low

### Principle 12: Constants Over Magic Values
**What to check**: Hardcoded numbers, strings used multiple times
**Look for**: Named constants with clear meaning
**Applies to**: All code
**Severity**: Low

### Principle 13: Comments Explain Why
**What to check**: Comment quality
**Look for**: Context, rationale, warnings (not repeating code)
**Applies to**: Complex logic, workarounds, business rules
**Severity**: Low

---

## Architecture Principles

### Principle 14: Layer Separation
**What to check**: Dependency boundaries
**Look for**: Clear separation between UI, business logic, data access
**Applies to**: Multi-layer applications
**Severity**: High

### Principle 15: Proper Dependency Direction
**What to check**: Import statements, dependency flow
**Look for**: High-level modules don't depend on low-level details
**Applies to**: All modules
**Severity**: High

### Principle 16: No Circular Dependencies
**What to check**: Module dependencies
**Look for**: A→B→C→A cycles
**Applies to**: All modules
**Severity**: High

---

## Testing Principles

### Principle 17: Tests Exist
**What to check**: New functionality has corresponding tests
**Look for**: Test files, test cases covering new code
**Applies to**: All new features, bug fixes
**Severity**: High

### Principle 18: Test Quality
**What to check**: Test names, coverage, edge cases
**Look for**: Descriptive names, happy + sad paths, boundary conditions
**Applies to**: All test files
**Severity**: Medium

### Principle 19: No Flaky Tests
**What to check**: Test determinism
**Look for**: No sleeps, no external dependencies without mocks, no order dependency
**Applies to**: All tests
**Severity**: High

---

## Performance Principles

### Principle 20: Efficient Data Access
**What to check**: Database queries, API calls in loops
**Look for**: N+1 patterns, missing eager loading
**Applies to**: Data access code
**Severity**: Medium

### Principle 21: Resource Cleanup
**What to check**: Files, connections, locks
**Look for**: Proper cleanup (context managers, finally blocks, defer)
**Applies to**: All resource usage
**Severity**: High

### Principle 22: Async Context Awareness
**What to check**: Blocking calls in async contexts
**Look for**: Proper async/await usage, non-blocking operations
**Applies to**: Async code (JavaScript, Python, Go)
**Severity**: High

---

## How to Apply These Principles

1. **Universal principles are always checked** - regardless of project stack
2. **Stack-specific standards come from active worker skills** - Code Reviewer dynamically loads these
3. **Project standards override when specified** - from project's `claude.md`

## Severity Mapping

| Severity | Definition | Blocks Approval |
|----------|------------|-----------------|
| **Critical** | Security vulnerability, data loss risk, breaking change | Yes |
| **High** | Bug, significant deviation from standards, missing tests | Yes |
| **Medium** | Code quality issue, maintainability concern | No (but noted) |
| **Low** | Style preference, suggestion | No |
