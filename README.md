# Vhape – Simplifying API Security for Junior Developers and Startup Founders

---

## About

Vhape is a university project developed for the *Data Structures and Compilers* course at Global University. It was inspired by the common problem faced by developers and startup founders: many people cannot validate the security of their APIs because they lack the necessary knowledge and time.

Vhape provides a minimalistic framework to **validate REST API authentication and authorization** using a **simple Domain-Specific Language (DSL)** and **BDD-style scenarios (Behave)**. This allows junior developers and non-technical founders to **quickly check if their APIs are secure**, without needing deep security expertise.

---

## Key Features

- **Simple DSL:** Use plain phrases like `valid token`, `expect 401`, `access denied`.
- **BDD with Behave:** Write and execute structured scenarios.
- **Multiple Scenarios Support:** Test several authentication cases in a single file.
- **Interactive Test Runner:** Select which features to run with an intuitive menu or command-line options.
- **Modern HTML Reports:** Beautiful, interactive web-based reports with search and filter capabilities.
- **JSON Reports:** Machine-readable reports for CI/CD integration.
- **Comprehensive Unit Tests:** 94+ unit tests covering parser, reporting, and core logic.
- **Modular & Extensible:** Parser, steps, and features are organized for future growth.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Angel-crypt/vhape-mvp.git
cd vhape-mvp
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv  # Linux/macOS
python -m venv venv   # Windows

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt

# (Optional) Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Start the Dummy API Server

```bash
# Method 1: Using bash script (recommended)
./api_dummy/run.sh

# Method 2: Using Python script
python api_dummy/run.py
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

> 📖 **For detailed API documentation**, see [`api_dummy/README.md`](api_dummy/README.md)

### 5. Run Tests

**Interactive Mode (Recommended):**

```bash
# Interactive menu to select which features to run
python tests/e2e/run_e2e_tests.py
```

**Command Line Options:**

```bash
# Run all features (skip interactive menu)
python tests/e2e/run_e2e_tests.py --all

# Run specific features
python tests/e2e/run_e2e_tests.py --features auth
python tests/e2e/run_e2e_tests.py --features auth,api_security

# See all options
python tests/e2e/run_e2e_tests.py --help
```

**Direct Behave Execution:**

```bash
# Run all features directly with Behave
behave features/

# Run specific feature
behave features/auth.feature
```

> 📖 **For test execution details and reports**, see [`tests/results/README.md`](tests/results/README.md)

---

## Project Structure

```
vhape-mvp/
├── api_dummy/              # Dummy API for testing (HU2)
│   └── README.md           # 📖 API documentation
├── vhape/                  # Core framework
│   ├── parser/             # DSL parser (Lark)
│   ├── reporting/          # Test reporting
│   └── README.md           # 📖 Framework documentation
├── features/               # BDD feature files (Gherkin)
│   └── steps/              # Step definitions
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── e2e/                # End-to-end tests
│   └── results/            # Test execution reports
│       └── README.md       # 📖 Reports documentation
└── docs/                   # Documentation
    ├── dsl-syntax.md       # DSL syntax reference
    └── dsl-keywords-reference.md  # Keywords quick reference
```

---

## Step-by-Step Guide

### Step 1: Configure API URL

Before running tests, configure the API URL you want to test. You can do this in two ways:

**Option A: Environment Variable (Recommended)**

```bash
# Set the API URL
export VHAPE_API_URL="http://localhost:8000"

# Or for Windows PowerShell
$env:VHAPE_API_URL="http://localhost:8000"

# Or for Windows CMD
set VHAPE_API_URL=http://localhost:8000
```

**Option B: Default Value**

If not set, Vhape defaults to `http://localhost:8000`. You can change this in `features/steps/auth_steps.py`:

```python
API_BASE_URL = os.getenv("VHAPE_API_URL", "http://your-api-url.com")
```

### Step 2: Create a Feature File

Create a new feature file in the `features/` directory:

```bash
# Create a new feature file
touch features/my_api_security.feature
# or
# On Windows: type nul > features\my_api_security.feature
```

**Feature File Structure:**

```gherkin
Feature: My API Security Tests
  As a developer
  I want to validate my API security
  So that I can ensure it's protected

  Scenario: Valid token should grant access
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token

  Scenario: Invalid token should return 401
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401

  Scenario: Admin can access admin endpoint
    Given I have an admin token
    When I send a request to "/api/admin/users"
    Then the response should access allowed

  Scenario: User cannot access admin endpoint
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access denied
```

### Step 3: Understanding DSL Keywords

**Given (Setup):**

- `I have a valid token` - Use a valid authentication token
- `I have an admin token` - Use an admin-level token
- `I have a user token` - Use a user-level token
- `I have an invalid token` - Use an invalid/expired token
- `I have no token` - Don't send any token

**When (Action):**

- `I send a request to "/your/endpoint"` - Send HTTP request to the endpoint

**Then (Validation):**

- `the response should validate token` - Expect 200 OK with valid response
- `the response should expect 401` - Expect 401 Unauthorized
- `the response should access denied` - Expect 403 Forbidden (access denied)
- `the response should access allowed` - Expect 200 OK (access granted)

> 📖 **For complete DSL syntax and keywords**, see:
>
> - [`docs/dsl-syntax.md`](docs/dsl-syntax.md) - Complete DSL syntax guide
> - [`docs/dsl-keywords-reference.md`](docs/dsl-keywords-reference.md) - Quick keyword reference

### Step 4: Run Your Tests

The `run_e2e_tests.py` script provides an interactive and flexible way to run your tests.

#### Interactive Mode (Default)

When you run the script without arguments, it shows an interactive menu:

```bash
python tests/e2e/run_e2e_tests.py
```

**Interactive Menu Options:**

- `[0]` - Run ALL features
- `[1-N]` - Select specific feature(s) by number (comma-separated, e.g., `1,3,5`)
- `[q]` - Quit

**Example Interactive Session:**

```
============================================================
  Select Features to Run
============================================================

Available features:

  [1] api_security.feature
  [2] auth.feature
  [3] edge_cases.feature
  [4] failure_scenarios.feature
  [5] workflow.feature

Options:
  [0]  Run ALL features
  [1-5] Select specific feature(s) (comma-separated, e.g., 1,3,5)
  [q]  Quit

Enter your choice: 1,2
```

#### Command Line Options

**Run all features (skip menu):**

```bash
python tests/e2e/run_e2e_tests.py --all
# or
python tests/e2e/run_e2e_tests.py -a
```

**Run specific features:**

```bash
# Single feature
python tests/e2e/run_e2e_tests.py --features auth
python tests/e2e/run_e2e_tests.py -f auth

# Multiple features
python tests/e2e/run_e2e_tests.py --features auth,api_security
python tests/e2e/run_e2e_tests.py -f auth,workflow
```

**View help:**

```bash
python tests/e2e/run_e2e_tests.py --help
```

#### Direct Behave Execution

You can also run Behave directly:

```bash
# Run all features
behave features/

# Run specific feature
behave features/my_api_security.feature

# Run with verbose output
behave features/my_api_security.feature --no-capture

# Run by tags
behave --tags=@smoke     # Run only smoke tests
behave --tags=@security  # Run only security tests
behave --tags=@negative  # Run failure scenarios
```

> **Note:** The `behave.ini` configuration file is located in `vhape/` directory. The script `run_e2e_tests.py` automatically handles copying it to the project root when needed. For direct `behave` commands from the project root, you may need to temporarily copy `vhape/behave.ini` to the root, or run `behave` from the `vhape/` directory.

### Step 5: Review Results

After running tests with `run_e2e_tests.py`, you'll get:

1. **Console Output:**

   ```
   ============================================================
     VHAPE - Security Test Summary
   ============================================================
   
   Features:
      Total:    1
      [OK] Passed: 1
      [FAIL] Failed: 0
   
   Scenarios:
      Total:    4
      [OK] Passed: 4
      [FAIL] Failed: 0
   
   Steps:
      Total:    12
      [OK] Passed: 12
      [FAIL] Failed: 0
   
   [OK] No security issues detected
   
   Success Rate: 100.0%
   Duration: 1.23s
   ```

2. **JSON Report:**
   - Location: `tests/results/summary_YYYYMMDD_HHMMSS.json`
   - Contains detailed test results, security issues, and statistics
   - Machine-readable format for CI/CD integration

3. **HTML Report (Automatically Generated):**
   - Location: `tests/results/summary_YYYYMMDD_HHMMSS.html`
   - Modern, interactive web-based report
   - Automatically opens in your default browser
   - Features:
     - Visual statistics dashboard
     - Search and filter functionality
     - Detailed feature and scenario breakdown
     - Security issues highlighting
     - Responsive design (mobile-friendly)

### Step 6: Customize for Your API

If your API uses different authentication (e.g., API keys, custom headers), you'll need to:

1. **Update token mapping** in `features/steps/auth_steps.py`:

   ```python
   TOKEN_MAP = {
       'valid': 'your-valid-token',
       'admin': 'your-admin-token',
       'user': 'your-user-token',
       'invalid': 'invalid-token-123'
   }
   ```

2. **Modify request headers** in `features/steps/auth_steps.py` if needed (currently uses `Authorization: Bearer <token>`)

3. **Adjust endpoint paths** in your feature files to match your API structure

---

## Usage Example

Here's a complete example feature file (`features/my_api.feature`):

```gherkin
Feature: My API Security Tests
  As a developer
  I want to validate my API security
  So that I can ensure it's protected

  Scenario: Valid token should grant access
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token

  Scenario: Invalid token should return 401
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401
```

---

## Module Documentation

### [`api_dummy/`](api_dummy/README.md) - Dummy API

The dummy API provides a controlled environment for testing DSL keywords. It simulates different authentication and authorization behaviors.

**See:** [`api_dummy/README.md`](api_dummy/README.md) for:

- Endpoints documentation
- Authentication tokens
- Execution instructions
- Postman collection

### [`vhape/`](vhape/README.md) - Core Framework

The core framework provides the DSL parser and reporting system.

**See:** [`vhape/README.md`](vhape/README.md) for:

- Parser DSL usage and examples
- Reporting system documentation
- Integration with Behave
- Extensibility guide

---

## Test Execution

### Running E2E Tests

**Interactive Mode (Recommended):**

```bash
# Shows interactive menu to select features
python tests/e2e/run_e2e_tests.py
```

**Command Line Options:**

```bash
# Run all features (skip menu)
python tests/e2e/run_e2e_tests.py --all

# Run specific features
python tests/e2e/run_e2e_tests.py --features auth
python tests/e2e/run_e2e_tests.py --features auth,api_security,workflow

# View help
python tests/e2e/run_e2e_tests.py --help
```

**Direct Behave Execution:**

```bash
# Run all features
behave features/

# Run specific feature
behave features/auth.feature

# Run failure scenarios (to test reporting with failures)
behave features/failure_scenarios.feature

# Run by tags
behave --tags=@negative  # Run failure scenarios
behave --tags=@smoke     # Run smoke tests only
behave --tags=@security  # Run security tests
```

### Running Unit Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_parser.py -v
pytest tests/unit/test_summary.py -v
pytest tests/unit/test_auth_steps.py -v

# Run with coverage
pytest tests/unit/ --cov=vhape --cov-report=html
```

### Test Reports

Reports are automatically generated in `tests/results/` directory:

1. **JSON Report** (`summary_YYYYMMDD_HHMMSS.json`):
   - Machine-readable format
   - Contains detailed test results, security issues, and statistics
   - Suitable for CI/CD integration

2. **HTML Report** (`summary_YYYYMMDD_HHMMSS.html`):
   - Modern, interactive web-based report
   - Automatically opens in your default browser
   - Features search, filters, and visual statistics
   - Responsive design for all devices

**See:** [`tests/results/README.md`](tests/results/README.md) for detailed report format and usage.

### Testing Failure Reporting

The project includes intentionally failing scenarios to verify that the reporting system works correctly with both successes and failures.

**Run failure scenarios:**

```bash
# Using the interactive runner
python tests/e2e/run_e2e_tests.py
# Then select option 4 (failure_scenarios.feature)

# Or using command line
python tests/e2e/run_e2e_tests.py --features failure_scenarios

# Or directly with Behave
behave features/failure_scenarios.feature
# or
behave --tags=@negative
```

This will execute 8 scenarios that intentionally fail, showing:

- [FAIL] Failed scenarios in the summary
- [WARN] Security issues detected
- Success rate calculation with failures
- Detailed error messages in reports

**Example failure report output:**

```
Features:
   Total:    5
   [OK] Passed: 4
   [FAIL] Failed: 1

Scenarios:
   Total:    36
   [OK] Passed: 28
   [FAIL] Failed: 8

Steps:
   Total:    108
   [OK] Passed: 100
   [FAIL] Failed: 8

[WARN] Security Issues Found: 8

Success Rate: 77.8%
```

---

## Dependencies

### Core Dependencies

- `behave==1.3.3` - BDD framework
- `requests==2.32.5` - HTTP client
- `lark-parser==0.12.0` - DSL parser
- `fastapi==0.119.1` - Dummy API framework
- `uvicorn==0.38.0` - ASGI server

### Development Dependencies

- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting

---

## Troubleshooting

### API Server Not Running

**Error:** `ConnectionError: API server is not running`

**Solution:** Start the dummy API server:

```bash
./api_dummy/run.sh
```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'behave'`

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

### Virtual Environment Issues

**Error:** Commands not found

**Solution:** Ensure virtual environment is activated:

```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

---

## Docker Execution Guide

Vhape can be run entirely in Docker containers, making it easy to set up and run tests without installing dependencies locally.

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

### Quick Start

**1. Build the Docker images:**

```bash
docker-compose build
```

**2. Start services in detached mode:**

```bash
docker-compose up -d
```

This will start:

- `api_dummy` service on port 8000
- `bjparser` service (ready to execute tests)

**3. Run tests:**

```bash
# Run all E2E tests
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --all

# Run specific features
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --features auth

# Run behave directly
docker-compose run --rm bjparser behave

# Interactive shell (for debugging)
docker-compose run --rm bjparser
```

**4. View results:**

Test results are automatically saved to `./tests/results/`:

- JSON reports: `./tests/results/summary_YYYYMMDD_HHMMSS.json`
- HTML reports: `./tests/results/summary_YYYYMMDD_HHMMSS.html`

**5. Cleanup:**

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
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

### Important Notes

⚠️ **Warning:** The dummy API uses hardcoded test tokens (`valid-token`, `user-token`) and is **NOT suitable for production use**. It is designed solely for testing the Vhape BDD framework.

---

## Documentation

- **[DSL Syntax Guide](docs/dsl-syntax.md)** - Complete DSL syntax reference
- **[DSL Keywords Reference](docs/dsl-keywords-reference.md)** - Quick keyword lookup
- **[API Dummy Documentation](api_dummy/README.md)** - Dummy API details and endpoints
- **[Vhape Framework Documentation](vhape/README.md)** - Parser and reporting system
- **[Test Results Documentation](tests/results/README.md)** - Report format and usage

---

## Contributing

This is a university project. For questions or suggestions, please open an issue.

---

## License

See [LICENSE](LICENSE) file for details.
