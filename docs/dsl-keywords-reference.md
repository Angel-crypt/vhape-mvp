# Vhape DSL - Keywords Reference

Quick reference guide for all available keywords in the Vhape DSL.

## Context Keywords (Given)

### Tokens

| Keyword | Description | Expected Result |
|---------|-------------|-----------------|
| `I have a valid token` | Valid token (admin) | Allows access |
| `I have an admin token` | Token with admin role | Allows admin access |
| `I have a user token` | Token with user role | Allows user access |
| `I have an invalid token` | Invalid token | Returns 401 |
| `I have no token` | No token | Returns 401 |
| `I have a missing token` | Missing token | Returns 401 |

## Action Keywords (When)

### Request

| Keyword | Format | Example |
|---------|--------|---------|
| `I send a request to "<endpoint>"` | Endpoint in quotes | `"/api/users/me"` |

## Validation Keywords (Then)

### Results

| Keyword | Description | Expected HTTP Code |
|---------|-------------|-------------------|
| `validate token` | Valid token | 200 OK |
| `expect 401` | Unauthorized | 401 Unauthorized |
| `access denied` | Access denied | 403 Forbidden |
| `access allowed` | Access allowed | 200 OK |

## Keyword to Endpoint Mapping

Based on the current dummy API:

| DSL Keyword | Endpoint | Test Case |
|------------|----------|-----------|
| `validate token` | `/api/users/me` | Valid token → 200 |
| `expect 401` | `/api/users/me` | No token or invalid token → 401 |
| `access denied` | `/api/admin/users` | User token in admin endpoint → 403 |
| `access allowed` | `/api/admin/users` | Admin token in admin endpoint → 200 |

## Quick Examples

### Validate Token

```gherkin
Given I have a valid token
When I send a request to "/api/users/me"
Then the response should validate token
```

### Expect 401

```gherkin
Given I have no token
When I send a request to "/api/users/me"
Then the response should expect 401
```

### Access Denied

```gherkin
Given I have a user token
When I send a request to "/api/admin/users"
Then the response should access denied
```

### Access Allowed

```gherkin
Given I have an admin token
When I send a request to "/api/admin/users"
Then the response should access allowed
```

## Related Documentation

- **[DSL Syntax Guide](dsl-syntax.md)** - Complete syntax reference
- **[Vhape Framework](README_vhape.md)** - Parser implementation
- **[API Dummy](README_api_dummy.md)** - Endpoint documentation
- **[Main README](../README.md)** - Project overview
