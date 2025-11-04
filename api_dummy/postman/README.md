# Postman Collection for Vhape Dummy API

Complete Postman collection and environment for testing all authentication scenarios of the Vhape dummy API.

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

The collection is organized in 3 folders:

### 1. Health Check
- `GET /api/health` - Verify that the server is running

**Expected:** Returns `200 OK` without authentication

### 2. Users - Get Current User Profile
- `GET /api/users/me` (with valid token) → `200` (validate token)
- `GET /api/users/me` (with invalid token) → `401` (expect 401)
- `GET /api/users/me` (without token) → `401` (expect 401)

**Expected:** Returns `200 OK` with valid token (validate token), `401 Unauthorized` with invalid token or no token (expect 401)

### 3. Admin - Get All Users
- `GET /api/admin/users` (with user token) → `403` (access denied)
- `GET /api/admin/users` (with admin token) → `200` (access allowed)

**Expected:** Returns `403 Forbidden` with user token (access denied), `200 OK` with admin token (access allowed)

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://localhost:8000` | API base URL |
| `valid_token` | `valid-token` | Admin user token |
| `user_token` | `user-token` | Regular user token |
| `invalid_token` | `invalid-token` | Invalid token for testing |
| `expired_token` | `expired-token` | Expired token for testing |

## Running Tests

### Run Individual Request

1. Select a request from the collection
2. Click **Send**
3. Review the **Test Results** tab to see validation results

### Run Complete Collection

1. Right-click on the collection name
2. Select **Run collection**
3. Click **Run Vhape Dummy API - Test Suite**
4. Review results of all tests

### Run with Collection Runner

1. Click **Collections** in the sidebar
2. Click **Run** next to the collection
3. Select which requests to run
4. Click **Run Vhape Dummy API**
5. View summary of results

## Test Scripts

Each request includes automated scripts that validate:

- ✅ **Status codes** - Verifies correct HTTP codes
- ✅ **Response structure** - Verifies expected JSON properties
- ✅ **Error messages** - Validates error detail messages
- ✅ **Data validation** - Ensures response data matches expectations

## DSL Keywords Testing

The collection includes specific endpoints for testing DSL keywords:

### `validate token`
- **Endpoint:** `GET /api/users/me`
- **Usage:** Valid token in Authorization header
- **Expected:** `200 OK` with user profile

### `expect 401`
- **Endpoint:** `GET /api/users/me`
- **Usage:** No token or with invalid token
- **Expected:** `401 Unauthorized`

### `access denied`
- **Endpoint:** `GET /api/admin/users`
- **Usage:** User token in admin endpoint
- **Expected:** `403 Forbidden`

### `access allowed`
- **Endpoint:** `GET /api/admin/users`
- **Usage:** Admin token in admin endpoint
- **Expected:** `200 OK`

## Status Code Reference

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| `200 OK` | Success | Valid token, authorized access |
| `401 Unauthorized` | Authentication failed | Invalid or missing token |
| `403 Forbidden` | Authorization failed | Valid token but insufficient permissions |

## Tips

1. **Check Environment**: Always ensure "Vhape Dummy API - Local" is selected
2. **Server Running**: Ensure the API server is running at `http://localhost:8000`
3. **View Results**: Click on any request and review the **Test Results** tab
4. **Modify Variables**: Edit environment variables if you need different tokens or URLs
5. **Export Results**: Use Postman's export function to save test results

## Troubleshooting

### Collection won't import
- Ensure you're using Postman v9.0 or later
- Verify that the JSON files are valid

### Tests are failing
- Verify that the API server is running: `./api_dummy/run.sh`
- Verify that the environment is selected
- Verify that `base_url` points to the correct server

### Variables aren't working
- Ensure the environment is selected in the dropdown
- Verify that variable names match exactly (case-sensitive)
- Verify that variables are enabled in the environment

## Next Steps

After importing and running the collection:

1. ✅ Verify that all tests pass
2. ✅ Review response structures
3. ✅ Test edge cases manually
4. ✅ Export results for documentation
5. ✅ Share collection with team members
