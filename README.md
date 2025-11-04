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
- **Clear Reporting:** Get understandable feedback about API security with JSON reports.
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

```bash
# Run all tests and generate reports (recommended)
python tests/e2e/run_tests_and_generate_report.py

# Or run Behave directly
behave features/
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

## Usage Example

Create a feature file (e.g., `features/my_api.feature`):

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

> 📖 **For complete DSL syntax and keywords**, see:
>
> - [`docs/dsl-syntax.md`](docs/dsl-syntax.md) - Complete DSL syntax guide
> - [`docs/dsl-keywords-reference.md`](docs/dsl-keywords-reference.md) - Quick keyword reference

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

### Running Tests

```bash
# Run all tests with report generation (recommended)
python tests/e2e/run_tests_and_generate_report.py

# Run specific feature
behave features/auth.feature

# Run failure scenarios (to test reporting with failures)
behave features/failure_scenarios.feature

# Run by tags
behave --tags=@negative  # Run failure scenarios
behave --tags=@smoke     # Run smoke tests only

# Run parser unit tests (requires pytest)
pytest tests/unit/test_parser.py -v
```

### Test Reports

Reports are automatically generated in `tests/results/` directory with JSON format.

**See:** [`tests/results/README.md`](tests/results/README.md) for report format and usage.

### Testing Failure Reporting

The project includes intentionally failing scenarios to verify that the reporting system works correctly with both successes and failures.

**Run failure scenarios:**

```bash
behave features/failure_scenarios.feature
# or
behave --tags=@negative
```

This will execute 8 scenarios that intentionally fail, showing:
- ❌ Failed scenarios in the summary
- ⚠️ Security issues detected
- 📊 Success rate calculation with failures
- 📝 Detailed error messages in reports

**Example failure report output:**

```
📋 Features:   Total: 5, ✅ Passed: 4, ❌ Failed: 1
🎯 Scenarios:  Total: 36, ✅ Passed: 28, ❌ Failed: 8
📝 Steps:      Total: 108, ✅ Passed: 100, ❌ Failed: 8
📊 Success Rate: 77.8%
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
