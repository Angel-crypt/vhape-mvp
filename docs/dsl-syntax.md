# Vhape DSL - Syntax Guide

## Overview

The Vhape DSL is based on Gherkin and allows you to describe API security scenarios in a simple and natural way. It's designed for non-technical users who need to validate their API security.

## Basic Structure

### Feature

Describes what functionality is being tested.

```gherkin
Feature: Feature Name
  Optional feature description
```

### Scenario

Describes a specific test case.

```gherkin
Scenario: Scenario Name
  Scenario steps
```

## Main DSL Keywords

### 1. `validate token`

Validates that an authentication token is valid.

**Example:**

```gherkin
Given I have a valid token
When I send a request to "/api/users/me"
Then the response should validate token
```

### 2. `expect 401`

Verifies that the response is 401 Unauthorized.

**Example:**

```gherkin
Given I have no token
When I send a request to "/api/users/me"
Then the response should expect 401
```

Or with invalid token:

```gherkin
Given I have an invalid token
When I send a request to "/api/users/me"
Then the response should expect 401
```

### 3. `access denied`

Verifies that the response is 403 Forbidden (access denied).

**Example:**

```gherkin
Given I have a user token
When I send a request to "/api/admin/users"
Then the response should access denied
```

### 4. `access allowed`

Verifies that the response is 200 OK (access allowed).

**Example:**

```gherkin
Given I have an admin token
When I send a request to "/api/admin/users"
Then the response should access allowed
```

## Step Structure

### Given

Defines the initial state or context.

**Available tokens:**

- `valid token` / `admin token` - Valid token with admin role
- `user token` - Valid token with user role
- `invalid token` - Invalid token
- `no token` / `missing token` - No token

**Examples:**

```gherkin
Given I have a valid token
Given I have an admin token
Given I have a user token
Given I have an invalid token
Given I have no token
```

### When

Defines the action to perform.

**Format:**

```gherkin
When I send a request to "<endpoint>"
```

**Examples:**

```gherkin
When I send a request to "/api/users/me"
When I send a request to "/api/admin/users"
```

### Then

Defines the expected result.

**Format:**

```gherkin
Then the response should <keyword>
```

**Available keywords:**

- `validate token` - Valid token (200 OK)
- `expect 401` - Unauthorized (401)
- `access denied` - Access denied (403)
- `access allowed` - Access allowed (200 OK)

**Examples:**

```gherkin
Then the response should validate token
Then the response should expect 401
Then the response should access denied
Then the response should access allowed
```

## Complete Examples

### Example 1: Validate Token

```gherkin
Feature: User Authentication
  As a developer
  I want to validate API authentication
  So that I can ensure my API is secure

  Scenario: Valid token should grant access
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token
```

### Example 2: Invalid Token

```gherkin
  Scenario: Invalid token should return 401
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401
```

### Example 3: No Token

```gherkin
  Scenario: Missing token should return 401
    Given I have no token
    When I send a request to "/api/users/me"
    Then the response should expect 401
```

### Example 4: Access Denied

```gherkin
Feature: Admin Authorization
  As a developer
  I want to validate admin authorization
  So that I can ensure admin endpoints are protected

  Scenario: User token should be denied access to admin endpoint
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access denied
```

### Example 5: Access Allowed

```gherkin
  Scenario: Admin token should allow access to admin endpoint
    Given I have an admin token
    When I send a request to "/api/admin/users"
    Then the response should access allowed
```

## Syntax Rules

1. **Case-insensitive**: Keywords can be written in uppercase or lowercase.
2. **Spaces**: Spaces are significant only within phrases.
3. **Quotes**: Endpoints must be enclosed in double quotes.
4. **Order**: Steps must follow the order Given → When → Then.

## Extensibility

The syntax is designed to be extensible. Future versions may add:

- Multiple headers
- HTTP methods (GET, POST, PUT, DELETE)
- Response body validation
- Timeouts
- Multiple requests in a scenario

## Implementation Notes

- The parser should be tolerant of minor variations (extra spaces, case differences)
- Endpoints can be relative or absolute
- Tokens are referenced by name, not by value (the system resolves them internally)

## Related Documentation

- **[DSL Keywords Reference](dsl-keywords-reference.md)** - Quick keyword lookup
- **[Vhape Framework](README_vhape.md)** - Parser implementation details
- **[Main README](../README.md)** - Project overview
