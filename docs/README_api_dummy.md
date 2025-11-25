# Vhape Dummy API

Simple and controlled dummy API for testing DSL keywords of the Vhape BDD framework. This API simulates different authentication and authorization behaviors to enable API security testing.

## Purpose

This module implements **HU2 (User Story 2)** of the Vhape project. It provides a controlled environment where the BDD system can send HTTP requests and receive responses (status codes) that simulate different authentication behaviors.

**Not visible to end users**, but as a developer you can use the web documentation provided by FastAPI to explore the endpoints.

## Features

- **3 essential endpoints** for testing DSL keywords
- **Automatic documentation** at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- **Simple predefined tokens** for testing
- **Simulated roles** (admin, user) for authorization testing
- **Controlled HTTP responses** (200, 401, 403) to validate the framework

## Architecture

```
api_dummy/
├── main.py              # Main FastAPI application
├── run.py               # Python script to run the server
├── run.sh               # Bash script to run the server
├── __init__.py          # Module initialization
└── postman/             # Postman collections for manual testing
    ├── Vhape_Dummy_API.postman_collection.json
    ├── Vhape_Dummy_API.postman_environment.json
    └── README.md
```

## DSL Keywords Tested

This API is specifically designed to test the following DSL keywords:

- **`validate token`** - Validates that an authentication token is valid (200 OK)
- **`expect 401`** - Verifies that 401 Unauthorized is returned (invalid or missing token)
- **`access denied`** - Verifies that 403 Forbidden is returned (access denied by role)
- **`access allowed`** - Verifies that access is allowed (200 OK with data)

## Running the API

### Prerequisites

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (if not installed)
pip install -r requirements.txt
```

### Method 1: Bash Script (Recommended)

```bash
./api_dummy/run.sh
```

### Method 2: Python Script

```bash
python api_dummy/run.py
```

### Method 3: Direct Uvicorn

```bash
python -m uvicorn api_dummy.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker Execution Guide

Vhape can be run entirely in Docker containers, making it easy to set up and run tests without installing dependencies locally.

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

### Quick Start with Docker

```bash
# 1. Build the Docker images
docker-compose build

# 2. Start services in detached mode
docker-compose up -d

# 3. Run tests
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --all
```

### Docker Services

**api_dummy:**

- FastAPI dummy API server
- Exposed on port 8000
- Health check endpoint: `/api/health`

**bjparser:**

- Vhape parser and Behave runner
- Waits for API dummy to be ready before executing
- Mounts `./tests/results` for persistent reports
- Supports interactive mode for debugging

### Running Tests with Docker

**Interactive Mode:**

```bash
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py
```

**Run All Features:**

```bash
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --all
```

**Run Specific Features:**

```bash
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --features auth,api_security
```

**Direct Behave Execution:**

```bash
docker-compose run --rm bjparser behave features/
```

**Unit Tests:**

```bash
docker-compose run --rm bjparser pytest tests/unit/ -v
```

### Viewing Results

Test results are automatically saved to `./tests/results/`:

- JSON reports: `./tests/results/summary_YYYYMMDD_HHMMSS.json`
- HTML reports: `./tests/results/summary_YYYYMMDD_HHMMSS.html`

### Environment Variables

Create a `.env` file (or use `.env.example` as a template):

```bash
VHAPE_API_URL=http://api_dummy:8000
RESULTS_DIR=./tests/results
```

### Troubleshooting

**API not ready:**
The bjparser container automatically waits up to 30 seconds for the API to be ready. If you see connection errors, check:

```bash
# Check API health
docker-compose exec api_dummy curl http://localhost:8000/api/health

# View API logs
docker-compose logs api_dummy
```

**Results not appearing:**
Ensure the `./tests/results` directory exists and is writable:

```bash
mkdir -p tests/results
chmod 755 tests/results
```

**Interactive debugging:**
Access an interactive shell in the bjparser container:

```bash
docker-compose run --rm bjparser
# Inside container:
python tests/e2e/run_e2e_tests.py --all
behave
python -c "import requests; print(requests.get('http://api_dummy:8000/api/health').status_code)"
```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### Important Notes

⚠️ **Warning:** The dummy API uses hardcoded test tokens (`valid-token`, `user-token`) and is **NOT suitable for production use**. It is designed solely for testing the Vhape BDD framework.

## Endpoints

### Health Check

```
GET /api/health
```

Public endpoint to verify that the server is running.

**Response:** `200 OK`

```json
{"status": "healthy"}
```

### Get Current User Profile

```
GET /api/users/me
Authorization: Bearer <token>
```

**DSL keywords:** `validate token` / `expect 401`

- **Valid token:** `valid-token` → `200 OK` (validate token)
- **Invalid token:** `invalid-token` → `401 Unauthorized` (expect 401)
- **No token:** → `401 Unauthorized` (expect 401)

**Example with valid token:**

```bash
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/users/me
```

**Response:** `200 OK`

```json
{
  "user_id": "user1",
  "role": "admin",
  "message": "User profile retrieved successfully"
}
```

### Get All Users (Admin Only)

```
GET /api/admin/users
Authorization: Bearer <token>
```

**DSL keyword:** `access denied`

- **Admin token:** `valid-token` → `200 OK` (access allowed)
- **User token:** `user-token` → `403 Forbidden` (access denied)
- **No token:** → `401 Unauthorized`

**Example with user token (expects 403):**

```bash
curl -H "Authorization: Bearer user-token" http://localhost:8000/api/admin/users
```

**Response:** `403 Forbidden`

```json
{
  "detail": "Access denied"
}
```

**Example with admin token (expects 200):**

```bash
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/admin/users
```

**Response:** `200 OK`

```json
{
  "users": [
    {"id": "user1", "role": "admin"},
    {"id": "user2", "role": "user"}
  ],
  "message": "Users list retrieved successfully",
  "accessed_by": "user1"
}
```

## Testing Tokens

### Valid Tokens

| Token | Role | Usage |
|-------|------|-------|
| `valid-token` | admin | Test admin access (200) |
| `user-token` | user | Test denied access (403) |

### Invalid Tokens

| Token | Result |
|-------|--------|
| `invalid-token` | 401 Unauthorized |
| `expired-token` | 401 Unauthorized |
| (no token) | 401 Unauthorized |

## Usage Examples

### Testing "validate token"

```bash
# Valid token (should return 200)
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/users/me

# Invalid token (should return 401)
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/users/me

# No token (should return 401)
curl http://localhost:8000/api/users/me
```

### Testing "expect 401"

```bash
# No token in /api/users/me (should return 401)
curl http://localhost:8000/api/users/me

# Invalid token in /api/users/me (should return 401)
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/users/me
```

### Testing "access denied"

```bash
# User token in admin endpoint (should return 403)
curl -H "Authorization: Bearer user-token" http://localhost:8000/api/admin/users

# Admin token (should return 200)
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/admin/users
```

## Interactive Documentation

Once the server is running:

- **Swagger UI:** <http://localhost:8000/docs>
- **ReDoc:** <http://localhost:8000/redoc>

## DSL Keywords Mapping

| DSL Keyword | Endpoint | Test Case |
|------------|----------|-----------|
| `validate token` | `/api/users/me` | Valid token → 200 |
| `expect 401` | `/api/users/me` | No token or invalid token → 401 |
| `access denied` | `/api/admin/users` | User token in admin endpoint → 403 |
| `access allowed` | `/api/admin/users` | Admin token in admin endpoint → 200 |

## Status Codes

- `200 OK` - Valid token and authorized access
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - Valid token but no permissions

## Development

This API is part of the Vhape MVP project and is used internally for BDD testing. It is not designed for production use.
