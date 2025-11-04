# Postman Collection for Vhape Dummy API

Complete Postman collection and environment for testing all authentication scenarios of the Vhape Dummy API.

## Files

- **Vhape_Dummy_API.postman_collection.json** - Complete test collection with all endpoints
- **Vhape_Dummy_API.postman_environment.json** - Environment variables with tokens and base URL

## Import Instructions

### Step 1: Import Collection

1. Open Postman
2. Click **Import** button (top left)
3. Click **Upload Files**
4. Select `Vhape_Dummy_API.postman_collection.json`
5. Click **Import**

### Step 2: Import Environment

1. Click **Import** button again
2. Click **Upload Files**
3. Select `Vhape_Dummy_API.postman_environment.json`
4. Click **Import**

### Step 3: Select Environment

1. In the top right corner, click the environment dropdown
2. Select **"Vhape Dummy API - Local"**

## Collection Structure

The collection is organized into 7 folders:

### 1. Public Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /public` - Public access endpoint

**Expected:** All return `200 OK` without authentication

### 2. Protected Endpoints - Valid Token
- `GET /protected` (with admin token)
- `GET /secure-data` (with user token)

**Expected:** All return `200 OK` with user information

### 3. Protected Endpoints - Invalid Token
- `GET /protected` (with invalid token) → `401`
- `GET /protected` (with expired token) → `401`
- `GET /protected` (with malformed token) → `401`

**Expected:** All return `401 Unauthorized`

### 4. Protected Endpoints - Missing Token
- `GET /protected` (no token) → `401`
- `GET /secure-data` (no token) → `401`

**Expected:** All return `401 Unauthorized`

### 5. Admin Endpoints - Valid Admin Token
- `GET /admin-only` (with admin token) → `200`
- `GET /admin/users` (with admin token) → `200`

**Expected:** All return `200 OK` with admin access

### 6. Admin Endpoints - Non-Admin Token (Access Denied)
- `GET /admin-only` (with user token) → `403`
- `GET /admin/users` (with user token) → `403`

**Expected:** All return `403 Forbidden` (Access Denied)

### 7. Test Scenario Endpoints - DSL Keywords
- `GET /test/validate-token` (valid token) → `200`
- `GET /test/expect-401` (invalid token) → `401`
- `GET /test/expect-401` (no token) → `401`
- `GET /test/access-denied` (non-admin token) → `403`
- `GET /test/missing-token` (no token) → `401`

**Expected:** Responses match DSL keyword expectations

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://localhost:8000` | API base URL |
| `valid_token_admin` | `valid-token-123` | Admin user token |
| `valid_token_user` | `valid-token-456` | Regular user token |
| `admin_token` | `admin-token` | Admin token |
| `invalid_token` | `invalid-token` | Invalid token for testing |
| `expired_token` | `expired-token` | Expired token for testing |
| `malformed_token` | `malformed-token` | Malformed token for testing |

## Running Tests

### Run Individual Request

1. Select a request from the collection
2. Click **Send**
3. Check the **Test Results** tab for validation results

### Run Entire Collection

1. Right-click on the collection name
2. Select **Run collection**
3. Click **Run Vhape Dummy API - Complete Test Suite**
4. Review test results for all requests

### Run with Collection Runner

1. Click **Collections** in the sidebar
2. Click **Run** next to the collection
3. Select which requests to run
4. Click **Run Vhape Dummy API**
5. View results summary

## Test Scripts

Each request includes automated test scripts that validate:

- ✅ **Status codes** - Verifies correct HTTP status codes
- ✅ **Response structure** - Checks for expected JSON properties
- ✅ **Error messages** - Validates error detail messages
- ✅ **Data validation** - Ensures response data matches expectations

## DSL Keyword Testing

The collection includes specific endpoints for testing DSL keywords:

### `validate token`
- **Endpoint:** `GET /test/validate-token`
- **Use:** Valid token in Authorization header
- **Expected:** `200 OK` with validation status

### `expect 401`
- **Endpoint:** `GET /test/expect-401`
- **Use:** Invalid token or no token
- **Expected:** `401 Unauthorized`

### `access denied`
- **Endpoint:** `GET /test/access-denied`
- **Use:** Non-admin token on admin endpoint
- **Expected:** `403 Forbidden`

## Status Code Reference

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| `200 OK` | Success | Valid token, authorized access |
| `401 Unauthorized` | Authentication failed | Invalid/missing token |
| `403 Forbidden` | Authorization failed | Valid token but insufficient permissions |

## Tips

1. **Check Environment**: Always ensure "Vhape Dummy API - Local" is selected
2. **Server Running**: Make sure the API server is running on `http://localhost:8000`
3. **View Test Results**: Click on any request and check the **Test Results** tab
4. **Modify Variables**: Edit environment variables if you need different tokens or URLs
5. **Export Results**: Use Postman's export feature to save test results

## Troubleshooting

### Collection won't import
- Ensure you're using Postman v9.0 or later
- Check that JSON files are valid

### Tests failing
- Verify the API server is running: `./api_dummy/run.sh`
- Check that the environment is selected
- Verify `base_url` points to the correct server

### Variables not working
- Ensure environment is selected in the dropdown
- Check that variable names match exactly (case-sensitive)
- Verify variables are enabled in the environment

## Next Steps

After importing and running the collection:

1. ✅ Verify all tests pass
2. ✅ Review response structures
3. ✅ Test edge cases manually
4. ✅ Export results for documentation
5. ✅ Share collection with team members

