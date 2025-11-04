# Vhape Dummy API - HU2

A FastAPI-based dummy API server for testing authentication and authorization scenarios in the Vhape BDD framework.

## Purpose

This dummy API provides a controlled environment for testing DSL keywords such as:

- `validate token` - Test token validation
- `expect 401` - Test unauthorized access scenarios
- `access denied` - Test forbidden access scenarios (403)

## Features

- **Multiple Authentication Scenarios**: Valid tokens, invalid tokens, missing tokens
- **Role-Based Access Control**: Admin and regular user roles
- **FastAPI Auto-Documentation**: Interactive API docs at `/docs`
- **Test Endpoints**: Specific endpoints for testing DSL keywords

## Running the API

### Quick Start (Recommended)

**Step 1:** Navigate to the project root

```bash
cd /home/angel/PycharmProjects/vhape-mvp
```

**Step 2:** Activate the virtual environment

```bash
source .venv/bin/activate
```

**Step 3:** Install dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

**Step 4:** Run the server using one of the methods below

---

### Method 1: Using the Bash Script (Easiest)

The bash script automatically activates the virtual environment and starts the server:

```bash
# From project root
./api_dummy/run.sh
```

**What it does:**

- Automatically detects and activates `.venv` or `venv`
- Uses `python -m uvicorn` (works even if uvicorn is not in PATH)
- Starts the server with auto-reload enabled

**Expected output:**

```
Starting Vhape Dummy API...
FastAPI docs will be available at: http://localhost:8000/docs
Press Ctrl+C to stop the server

Activating virtual environment...
Starting server...
INFO:     Will watch for changes in these directories: ['/home/angel/PycharmProjects/vhape-mvp']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using StatReload
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### Method 2: Using the Python Runner

```bash
# From project root (with venv activated)
python api_dummy/run.py
```

Or make it executable:

```bash
chmod +x api_dummy/run.py
./api_dummy/run.py
```

---

### Method 3: Manual Uvicorn Command

**With virtual environment activated:**

```bash
# From project root
python -m uvicorn api_dummy.main:app --reload --host 0.0.0.0 --port 8000
```

Or if uvicorn is in your PATH:

```bash
uvicorn api_dummy.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Method 4: Direct Python Module Execution

```bash
# From project root (with venv activated)
python -m api_dummy.main
```

---

### Troubleshooting

**If you get "uvicorn: command not found":**

- Make sure the virtual environment is activated: `source .venv/bin/activate`
- Use `python -m uvicorn` instead of `uvicorn`
- Or use the bash script: `./api_dummy/run.sh` (it handles this automatically)

**If you get "ModuleNotFoundError: No module named 'fastapi'":**

- Activate virtual environment: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**If port 8000 is already in use:**

- Change the port in the command: `--port 8001`
- Or stop the process using port 8000

## Accessing the API

Once the server is running, you'll see output like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Access the API at:**

- **API Base URL**: <http://localhost:8000>
- **Swagger UI (Interactive Docs)**: <http://localhost:8000/docs> ⭐ **Recommended for testing**
- **ReDoc (Alternative Docs)**: <http://localhost:8000/redoc>
- **Health Check**: <http://localhost:8000/health>
- **OpenAPI JSON**: <http://localhost:8000/openapi.json>

**To stop the server:** Press `Ctrl+C` in the terminal where it's running.

## Authentication

The API uses Bearer token authentication via the `Authorization` header:

```
Authorization: Bearer <token>
```

### Valid Tokens

- `valid-token-123` - Admin user
- `valid-token-456` - Regular user
- `admin-token` - Admin user

### Invalid Tokens (for testing)

- `invalid-token` - Returns 401
- `expired-token` - Returns 401 with "Token has expired"
- `malformed-token` - Returns 401 with "Malformed token format"

## Endpoints

### Public Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /public` - Public access endpoint

### Protected Endpoints

- `GET /protected` - Requires valid token
- `GET /secure-data` - Requires valid token
- `GET /admin-only` - Requires admin role (403 for non-admin)
- `GET /admin/users` - Requires admin role (403 for non-admin)

### Test Scenarios Endpoints

- `GET /test/validate-token` - Test token validation
- `GET /test/expect-401` - Test 401 scenarios
- `GET /test/access-denied` - Test 403 scenarios
- `GET /test/missing-token` - Test missing token scenario

## Testing Examples

### Using curl

```bash
# Test with valid token
curl -H "Authorization: Bearer valid-token-123" http://localhost:8000/protected

# Test with invalid token (expect 401)
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/protected

# Test without token (expect 401)
curl http://localhost:8000/protected

# Test admin endpoint with non-admin token (expect 403)
curl -H "Authorization: Bearer valid-token-456" http://localhost:8000/admin-only

# Test admin endpoint with admin token (expect 200)
curl -H "Authorization: Bearer admin-token" http://localhost:8000/admin-only
```

### Using FastAPI Docs

1. Navigate to <http://localhost:8000/docs>
2. Click on any endpoint
3. Click "Try it out"
4. Add Authorization header: `Bearer valid-token-123`
5. Click "Execute"

## DSL Keyword Mapping

| DSL Keyword | Endpoint | Test Case |
|------------|----------|-----------|
| `validate token` | `/test/validate-token` | Use valid token |
| `expect 401` | `/test/expect-401` | Omit token or use invalid token |
| `access denied` | `/test/access-denied` | Use non-admin token on admin endpoint |

## Status Codes

- `200 OK` - Request successful
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Valid token but insufficient permissions

## Development

This API is part of the Vhape MVP project and is used internally for BDD testing. It is not intended for production use.
