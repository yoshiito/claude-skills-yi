# Edge Case Discovery Techniques

Systematic approaches to finding edge cases that need testing.

## Boundary Value Analysis

Test at boundaries, just inside, and just outside:

### Numeric Boundaries
```python
# For a function accepting age 0-120
test_age_zero()           # Lower boundary
test_age_one()            # Just inside lower
test_age_minus_one()      # Just outside lower
test_age_120()            # Upper boundary
test_age_119()            # Just inside upper
test_age_121()            # Just outside upper
```

### String Length Boundaries
```python
# For a field with max length 255
test_empty_string()       # Empty
test_one_char()           # Minimum content
test_254_chars()          # Just under limit
test_255_chars()          # At limit
test_256_chars()          # Over limit
test_very_long_string()   # Way over limit (10000 chars)
```

### Collection Boundaries
```python
test_empty_list()         # Empty collection
test_one_item()           # Single item
test_many_items()         # Normal case
test_max_items()          # At limit
test_over_limit()         # Exceeds limit
```

### Date/Time Boundaries
```python
test_past_date()          # Before valid range
test_today()              # Current day
test_future_date()        # After valid range
test_epoch()              # Unix epoch (1970-01-01)
test_year_2038()          # 32-bit overflow
test_leap_year()          # Feb 29
test_timezone_edge()      # DST transition
```

## Equivalence Partitioning

Group inputs into classes that should behave the same way:

### Status Field Example
```python
# Valid statuses (one test per partition)
test_status_active()      # Partition: active states
test_status_inactive()    # Partition: inactive states
test_status_pending()     # Partition: transitional states

# Invalid statuses
test_status_empty()       # Partition: empty/null
test_status_unknown()     # Partition: not in enum
test_status_wrong_type()  # Partition: type error
```

## State Transition Testing

For stateful systems, test all valid and invalid transitions:

```python
# Valid transitions
test_pending_to_active()
test_active_to_inactive()
test_inactive_to_archived()

# Invalid transitions
test_pending_to_archived()      # Skip states
test_archived_to_active()       # Reverse flow
test_deleted_to_anything()      # Terminal state

# Edge cases
test_transition_twice()         # Idempotent
test_concurrent_transitions()   # Race conditions
```

## Error Guessing

Common patterns that often have bugs:
- Off-by-one errors in loops/indexes
- Null/undefined handling
- Timezone conversions
- Character encoding (Unicode, emoji)
- Floating point precision
- Integer overflow
- Concurrent access to shared state
- Resource cleanup (connections, files)
- Cascading deletes
- Cache invalidation

### Test for These Specifically
```python
test_unicode_in_name()           # 名前, François
test_sql_injection_attempt()     # "Robert'); DROP TABLE--"
test_xss_attempt()               # <script>alert('XSS')</script>
test_very_long_input()           # DoS via large payloads
test_null_bytes()                # \x00 in strings
test_negative_numbers()          # When only positive expected
test_concurrent_updates()        # Race conditions
test_orphaned_records()          # Parent deleted, child remains
```

## Input Combination Testing

Test combinations of inputs, not just individual fields:

```python
test_valid_email_invalid_phone()
test_max_length_name_max_length_description()  # Both at limit
test_future_start_date_past_end_date()         # Date logic
test_optional_field_A_requires_field_B()       # Conditional requirements
```

## Negative Testing

Test what the system should NOT allow:

### Access Control
```python
test_user_cannot_access_other_user_data()
test_user_cannot_escalate_permissions()
test_deleted_user_cannot_login()
```

### Data Integrity
```python
test_cannot_create_duplicate_email()
test_cannot_delete_in_use_resource()
test_cannot_exceed_quota()
```

### Business Rules
```python
test_cannot_book_past_date()
test_cannot_withdraw_more_than_balance()
test_cannot_submit_after_deadline()
```

## LLM Blind Spots

LLMs often miss these scenarios - explicitly prompt for them:

### 1. Concurrent Operations
```
Test concurrent scenarios:
- Two users creating projects with same name simultaneously
- User updating project while another reads it
- Race condition on quota checks
```

### 2. Idempotency
```
Test idempotent operations:
- Deleting same resource twice
- Updating resource to same values
- Creating resource that already exists (if should be idempotent)
```

### 3. Cascading Effects
```
Test cascading behaviors:
- What happens to child resources when parent deleted?
- What happens to related resources?
- Verify soft-deleted resources don't appear in lists
```

### 4. Special Characters
```
Test with special characters:
- Unicode: 名前, François, emoji
- SQL injection attempts: "Robert'); DROP TABLE--"
- XSS attempts: <script>alert('XSS')</script>
- Null bytes: "test\x00name"
```

### 5. Timezone Edge Cases
```
Test timezone handling:
- UTC timestamps
- Daylight saving time transitions
- Different client timezones
- Leap seconds
```

### 6. Quota and Rate Limits
```
Test limits:
- User at quota limit
- User exceeding rate limit
- Bulk operations near limits
```

## Edge Case Checklist

- [ ] Boundary values tested
- [ ] Empty/null inputs tested
- [ ] Maximum length inputs tested
- [ ] Invalid type inputs tested
- [ ] Special characters tested
- [ ] Concurrent operations tested
- [ ] State transitions tested
- [ ] Security scenarios (SQLi, XSS) tested
- [ ] Cascading effects tested
- [ ] Timezone handling tested
