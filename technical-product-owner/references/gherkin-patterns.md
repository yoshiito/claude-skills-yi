# Gherkin Acceptance Criteria Patterns

Patterns for writing testable acceptance criteria using Given/When/Then syntax.

## Structure

```gherkin
AC-[ID]: [Descriptive Name]

Scenario: [Specific, testable scenario]
  Given [precondition - system state before action]
  And [additional precondition if needed]
  When [action - what the user/system does]
  And [additional action if needed]
  Then [outcome - observable result]
  And [additional outcome if needed]
```

## Rules for Good Gherkin

1. **One scenario per AC** - Don't combine multiple test cases
2. **Specific values** - Use concrete examples, not placeholders
3. **Observable outcomes** - Results must be verifiable
4. **No implementation details** - Describe behavior, not code
5. **Independent scenarios** - Each AC stands alone

---

## Happy Path Patterns

### Create Resource
```gherkin
AC-001: Successful resource creation

Scenario: User creates a new project with valid data
  Given an authenticated user on the projects page
  And the user has not exceeded their project quota
  When the user clicks "New Project"
  And enters "Q1 Marketing Campaign" as the project name
  And enters "Campaign planning for Q1 launch" as the description
  And clicks "Create"
  Then the project is created with status "active"
  And the user is redirected to the project detail page
  And a success message "Project created" is displayed
  And the project appears in the user's project list
```

### Read/List Resources
```gherkin
AC-002: List user's resources with pagination

Scenario: User views paginated list of their projects
  Given an authenticated user with 25 projects
  When the user navigates to the projects page
  Then the first 10 projects are displayed
  And projects are sorted by created_at descending
  And pagination shows "Page 1 of 3"
  And "Next" button is enabled
  And "Previous" button is disabled
```

### Update Resource
```gherkin
AC-003: Successful resource update

Scenario: User updates project name
  Given an authenticated user
  And a project "Old Name" owned by the user
  When the user opens the project settings
  And changes the name to "New Name"
  And clicks "Save"
  Then the project name is updated to "New Name"
  And updated_at timestamp is refreshed
  And a success message "Project updated" is displayed
```

### Delete Resource
```gherkin
AC-004: Soft delete resource

Scenario: User deletes a project
  Given an authenticated user
  And a project "To Delete" owned by the user
  When the user clicks "Delete Project"
  And confirms the deletion
  Then the project is marked as deleted (soft delete)
  And the project no longer appears in the project list
  And the project data is retained for 30 days
  And a success message "Project deleted" is displayed
```

---

## Validation Error Patterns

### Required Field Missing
```gherkin
AC-010: Missing required field rejected

Scenario: User submits form without required name field
  Given an authenticated user on the create project page
  When the user leaves the name field empty
  And clicks "Create"
  Then the form is not submitted
  And an error "Name is required" is displayed below the name field
  And the name field is highlighted in red
  And focus moves to the name field
```

### Field Exceeds Maximum Length
```gherkin
AC-011: Field exceeding max length rejected

Scenario: User enters name exceeding 255 characters
  Given an authenticated user on the create project page
  When the user enters a 300-character string in the name field
  And clicks "Create"
  Then the form is not submitted
  And an error "Name must be 255 characters or less" is displayed
```

### Invalid Format
```gherkin
AC-012: Invalid email format rejected

Scenario: User enters malformed email address
  Given a user on the registration page
  When the user enters "not-an-email" in the email field
  And clicks "Register"
  Then the form is not submitted
  And an error "Please enter a valid email address" is displayed
```

### Business Rule Violation
```gherkin
AC-013: Business rule constraint enforced

Scenario: User attempts to set negative price
  Given an authenticated admin on the product edit page
  When the user enters "-50" in the price field
  And clicks "Save"
  Then the form is not submitted
  And an error "Price cannot be negative" is displayed
```

---

## Authentication Patterns

### Unauthenticated Access
```gherkin
AC-020: Unauthenticated request rejected

Scenario: Anonymous user attempts to access protected resource
  Given a user who is not logged in
  When the user navigates to /projects
  Then the user is redirected to /login
  And the original URL is preserved for post-login redirect
  And no project data is exposed
```

### Session Expiration
```gherkin
AC-021: Expired session handled gracefully

Scenario: User's session expires during activity
  Given an authenticated user viewing their projects
  And the user's session has expired
  When the user clicks "New Project"
  Then the user is redirected to /login
  And a message "Your session has expired. Please log in again." is displayed
  And the attempted action URL is preserved
```

---

## Authorization Patterns

### Resource Ownership
```gherkin
AC-030: User cannot access other user's resource

Scenario: User attempts to view another user's project
  Given user A is authenticated
  And project "Secret Project" is owned by user B
  When user A navigates to /projects/{secret-project-id}
  Then a 404 Not Found response is returned
  And no data about the project is exposed
  And the attempt is logged for security audit
```

### Role-Based Access
```gherkin
AC-031: Non-admin cannot access admin function

Scenario: Regular user attempts admin action
  Given a user with role "member" is authenticated
  When the user attempts to access /admin/users
  Then a 403 Forbidden response is returned
  And a message "You don't have permission to access this page" is displayed
```

---

## Edge Case Patterns

### Empty State
```gherkin
AC-040: Empty state displayed when no data exists

Scenario: New user views empty project list
  Given an authenticated user with no projects
  When the user navigates to /projects
  Then an empty state illustration is displayed
  And the message "No projects yet" is shown
  And a "Create your first project" button is displayed
```

### Boundary Values
```gherkin
AC-041: Maximum allowed value accepted

Scenario: User creates project with maximum length name
  Given an authenticated user on the create project page
  When the user enters exactly 255 characters in the name field
  And clicks "Create"
  Then the project is created successfully
  And the full 255-character name is stored
```

### Concurrent Modification
```gherkin
AC-042: Concurrent edit conflict handled

Scenario: Two users edit same resource simultaneously
  Given user A and user B are viewing project "Shared"
  And user A changes the name to "Name A" and saves
  When user B (with stale data) changes name to "Name B" and saves
  Then user B receives a conflict error
  And user B is shown the current name "Name A"
  And user B is prompted to reload and retry
```

### Special Characters
```gherkin
AC-043: Unicode characters handled correctly

Scenario: User creates project with Unicode name
  Given an authenticated user on the create project page
  When the user enters "プロジェクト 🚀 Проект" as the name
  And clicks "Create"
  Then the project is created successfully
  And the name is stored and displayed correctly with all characters
```

---

## Error Recovery Patterns

### Network Failure
```gherkin
AC-050: Network error handled gracefully

Scenario: Network fails during form submission
  Given an authenticated user submitting a form
  And the network connection fails
  When the request times out after 30 seconds
  Then an error "Unable to connect. Please check your connection." is displayed
  And the form data is preserved
  And a "Retry" button is displayed
```

### Rate Limiting
```gherkin
AC-051: Rate limit communicated clearly

Scenario: User exceeds rate limit
  Given an authenticated user
  And the user has made 100 requests in the last minute
  When the user makes another request
  Then a 429 response is returned
  And a message "Too many requests. Please wait 60 seconds." is displayed
  And the Retry-After header indicates when to retry
```

---

## Anti-Patterns to Avoid

### Too Vague
```gherkin
# BAD - not testable
Scenario: User can create a project
  When the user creates a project
  Then it works
```

### Implementation Details
```gherkin
# BAD - describes code, not behavior
Scenario: Create project
  When POST /api/projects is called with JSON body
  Then the database INSERT query executes
  And a 201 response with JSON is returned
```

### Multiple Scenarios Combined
```gherkin
# BAD - should be separate ACs
Scenario: User creates, updates, and deletes project
  When the user creates a project
  Then it is created
  When the user updates the project
  Then it is updated
  When the user deletes the project
  Then it is deleted
```
