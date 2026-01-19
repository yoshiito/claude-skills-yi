# GitHub GraphQL Helpers for Issue Relationships

This reference provides reusable patterns for working with GitHub's Sub-Issues API (beta feature).

## Prerequisites

- GitHub CLI (`gh`) installed
- Access to repository
- Beta feature header: `-H "GraphQL-Features: sub_issues"`

## Core Concepts

### Node IDs vs Issue Numbers

GitHub GraphQL API requires **node IDs** (global identifiers), not issue numbers.

- Issue number: `123` (repository-specific)
- Node ID: `I_kwDOABcDef4AbCdEf` (global, starts with `I_` for issues)

**Get node ID from issue number:**
```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
node_id=$(gh api repos/$REPO/issues/123 --jq '.node_id')
```

## Helper Functions

### Function: Get Issue Node ID

```bash
# Get node ID for an issue
get_issue_node_id() {
  local issue_number=$1
  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
  gh api repos/$repo/issues/$issue_number --jq '.node_id'
}

# Usage:
parent_node=$(get_issue_node_id 101)
```

### Function: Set Parent-Child Relationship

```bash
# Add sub-issue relationship
add_sub_issue() {
  local parent_num=$1
  local child_num=$2

  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
  local parent_node=$(gh api repos/$repo/issues/$parent_num --jq '.node_id')
  local child_node=$(gh api repos/$repo/issues/$child_num --jq '.node_id')

  gh api graphql -H "GraphQL-Features: sub_issues" -f query='
    mutation {
      addSubIssue(input: {
        issueId: "'"$parent_node"'"
        subIssueId: "'"$child_node"'"
      }) {
        issue {
          number
          title
        }
        subIssue {
          number
          title
        }
      }
    }'
}

# Usage:
add_sub_issue 101 102  # Makes #102 a child of #101
```

### Function: Set Blocked-By Relationship

```bash
# Add blocked-by relationship
add_blocked_by() {
  local blocked_num=$1
  local blocker_num=$2

  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
  local blocked_node=$(gh api repos/$repo/issues/$blocked_num --jq '.node_id')
  local blocker_node=$(gh api repos/$repo/issues/$blocker_num --jq '.node_id')

  gh api graphql -H "GraphQL-Features: sub_issues" -f query='
    mutation {
      addBlockedBy(input: {
        issueId: "'"$blocked_node"'"
        blockingIssueId: "'"$blocker_node"'"
      }) {
        issue {
          number
          title
          blockedByIssues(first: 10) {
            nodes {
              number
              title
            }
          }
        }
      }
    }'
}

# Usage:
add_blocked_by 103 102  # Issue #103 is blocked by #102
```

### Function: Remove Parent-Child Relationship

```bash
# Remove sub-issue relationship
remove_sub_issue() {
  local parent_num=$1
  local child_num=$2

  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
  local parent_node=$(gh api repos/$repo/issues/$parent_num --jq '.node_id')
  local child_node=$(gh api repos/$repo/issues/$child_num --jq '.node_id')

  gh api graphql -H "GraphQL-Features: sub_issues" -f query='
    mutation {
      removeSubIssue(input: {
        issueId: "'"$parent_node"'"
        subIssueId: "'"$child_node"'"
      }) {
        issue {
          number
          title
        }
      }
    }'
}

# Usage:
remove_sub_issue 101 102
```

### Function: Remove Blocked-By Relationship

```bash
# Remove blocked-by relationship
remove_blocked_by() {
  local blocked_num=$1
  local blocker_num=$2

  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
  local blocked_node=$(gh api repos/$repo/issues/$blocked_num --jq '.node_id')
  local blocker_node=$(gh api repos/$repo/issues/$blocker_num --jq '.node_id')

  gh api graphql -H "GraphQL-Features: sub_issues" -f query='
    mutation {
      removeBlockedBy(input: {
        issueId: "'"$blocked_node"'"
        blockingIssueId: "'"$blocker_node"'"
      }) {
        issue {
          number
          title
        }
      }
    }'
}

# Usage:
remove_blocked_by 103 102
```

### Function: Query Issue Relationships

```bash
# Get all relationships for an issue
get_issue_relationships() {
  local issue_number=$1
  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
  local owner="${repo%/*}"
  local name="${repo#*/}"

  gh api graphql -H "GraphQL-Features: sub_issues" -f query='
    query {
      repository(owner: "'"$owner"'", name: "'"$name"'") {
        issue(number: '$issue_number') {
          number
          title
          state
          parent {
            number
            title
            state
          }
          subIssues(first: 20) {
            nodes {
              number
              title
              state
            }
          }
          blockedByIssues(first: 20) {
            nodes {
              number
              title
              state
            }
          }
        }
      }
    }'
}

# Usage:
get_issue_relationships 102 | jq '.data.repository.issue'
```

### Function: Check If Issue Is Blocked

```bash
# Returns true if issue has any open blockers
is_issue_blocked() {
  local issue_number=$1
  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
  local owner="${repo%/*}"
  local name="${repo#*/}"

  local result=$(gh api graphql -H "GraphQL-Features: sub_issues" -f query='
    query {
      repository(owner: "'"$owner"'", name: "'"$name"'") {
        issue(number: '$issue_number') {
          blockedByIssues(first: 20) {
            nodes {
              state
            }
          }
        }
      }
    }' --jq '.data.repository.issue.blockedByIssues.nodes[] | select(.state == "OPEN")')

  if [ -n "$result" ]; then
    return 0  # true - has open blockers
  else
    return 1  # false - no open blockers
  fi
}

# Usage:
if is_issue_blocked 103; then
  echo "Issue #103 is blocked"
else
  echo "Issue #103 is ready to work on"
fi
```

## Complete Workflows

### Workflow 1: Create Feature with Sub-Issues

```bash
#!/bin/bash
# Create a parent feature with sub-issues and relationships

# 1. Create parent issue
parent_num=$(gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "Full password reset functionality" \
  --label "feature" \
  --milestone "Auth Sprint" | grep -oP '\d+')

echo "Created parent issue #$parent_num"

# 2. Create sub-issues
backend_num=$(gh issue create \
  --title "[Backend] Password reset API" \
  --body "Implement reset API endpoint" \
  --label "backend" | grep -oP '\d+')

frontend_num=$(gh issue create \
  --title "[Frontend] Password reset form" \
  --body "Create reset form UI" \
  --label "frontend" | grep -oP '\d+')

echo "Created sub-issues #$backend_num and #$frontend_num"

# 3. Set parent-child relationships
add_sub_issue $parent_num $backend_num
add_sub_issue $parent_num $frontend_num

# 4. Set blocking relationship (frontend blocked by backend)
add_blocked_by $frontend_num $backend_num

echo "Relationships set successfully!"
echo "Parent: #$parent_num"
echo "  - Backend: #$backend_num"
echo "  - Frontend: #$frontend_num (blocked by #$backend_num)"
```

### Workflow 2: Query and Display Relationships

```bash
#!/bin/bash
# Display all relationships for an issue

issue_num=$1

echo "Fetching relationships for issue #$issue_num..."

result=$(get_issue_relationships $issue_num)

# Extract and display
echo "$(echo "$result" | jq -r '.data.repository.issue |
  "Issue #\(.number): \(.title) [\(.state)]"')"

parent=$(echo "$result" | jq -r '.data.repository.issue.parent |
  if . then "Parent: #\(.number) - \(.title)" else "Parent: None" end')
echo "$parent"

sub_issues=$(echo "$result" | jq -r '.data.repository.issue.subIssues.nodes[] |
  "  - Sub-issue: #\(.number) - \(.title) [\(.state)]"')
if [ -n "$sub_issues" ]; then
  echo "Sub-issues:"
  echo "$sub_issues"
fi

blockers=$(echo "$result" | jq -r '.data.repository.issue.blockedByIssues.nodes[] |
  "  - Blocked by: #\(.number) - \(.title) [\(.state)]"')
if [ -n "$blockers" ]; then
  echo "Blockers:"
  echo "$blockers"
fi
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "GraphQL: Could not resolve to an issue" | Invalid issue number | Verify issue exists with `gh issue view NUMBER` |
| "Missing header" | Forgot beta header | Add `-H "GraphQL-Features: sub_issues"` |
| "Invalid node ID" | Wrong node ID format | Use `gh api repos/OWNER/REPO/issues/N --jq '.node_id'` |
| "Issues must be in same repository" | Cross-repo relationships attempted | Only same-repo relationships supported |

### Error Handling Pattern

```bash
# Robust function with error handling
add_sub_issue_safe() {
  local parent_num=$1
  local child_num=$2

  # Validate inputs
  if [ -z "$parent_num" ] || [ -z "$child_num" ]; then
    echo "Error: Issue numbers required" >&2
    return 1
  fi

  # Get repo info
  local repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)
  if [ $? -ne 0 ]; then
    echo "Error: Not in a GitHub repository" >&2
    return 1
  fi

  # Get node IDs
  local parent_node=$(gh api repos/$repo/issues/$parent_num --jq '.node_id' 2>/dev/null)
  if [ $? -ne 0 ]; then
    echo "Error: Parent issue #$parent_num not found" >&2
    return 1
  fi

  local child_node=$(gh api repos/$repo/issues/$child_num --jq '.node_id' 2>/dev/null)
  if [ $? -ne 0 ]; then
    echo "Error: Child issue #$child_num not found" >&2
    return 1
  fi

  # Execute mutation
  local result=$(gh api graphql -H "GraphQL-Features: sub_issues" -f query='
    mutation {
      addSubIssue(input: {
        issueId: "'"$parent_node"'"
        subIssueId: "'"$child_node"'"
      }) {
        issue { number }
        subIssue { number }
      }
    }' 2>&1)

  if echo "$result" | grep -q "errors"; then
    echo "Error: GraphQL mutation failed" >&2
    echo "$result" | jq '.errors' >&2
    return 1
  fi

  echo "Successfully set #$child_num as sub-issue of #$parent_num"
  return 0
}
```

## Testing

### Verify Relationship Was Set

```bash
# After setting a relationship, verify it
verify_parent_child() {
  local parent_num=$1
  local child_num=$2

  local result=$(get_issue_relationships $child_num)
  local actual_parent=$(echo "$result" | jq -r '.data.repository.issue.parent.number // "none"')

  if [ "$actual_parent" = "$parent_num" ]; then
    echo "✅ Verified: #$child_num has parent #$parent_num"
    return 0
  else
    echo "❌ Failed: #$child_num parent is #$actual_parent, expected #$parent_num"
    return 1
  fi
}

# Usage:
add_sub_issue 101 102
verify_parent_child 101 102
```

## Best Practices

1. **Always use helper functions** - Reduces errors and improves readability
2. **Verify relationships after creation** - GraphQL mutations can silently fail
3. **Handle errors gracefully** - Check return codes and validate inputs
4. **Use descriptive variable names** - `parent_node` vs `child_node` instead of `node1`, `node2`
5. **Document the beta header requirement** - Always include `-H "GraphQL-Features: sub_issues"`
6. **Cache node IDs when possible** - Reduces API calls for bulk operations

## Debugging

### Enable verbose output

```bash
# Add --verbose to gh commands for debugging
gh api graphql --verbose -H "GraphQL-Features: sub_issues" -f query='...'

# View raw GraphQL response
get_issue_relationships 102 | jq '.'
```

### Check if beta feature is enabled

```bash
# Try a simple query to test access
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
  query {
    viewer {
      login
    }
  }
}'
```

## Additional Resources

- GitHub GraphQL API Explorer: https://docs.github.com/en/graphql/overview/explorer
- GitHub CLI Manual: https://cli.github.com/manual/
- GraphQL Sub-Issues mutation schema: Use `gh api graphql` with introspection queries
