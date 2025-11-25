# Project Structure

Complete overview of the Vhape project directory structure, files, and their purposes.

## Directory Tree

```
vhape-mvp/
├── api_dummy/                    # Dummy API for testing (HU2)
│   ├── __init__.py              # Module initialization
│   ├── main.py                  # FastAPI application
│   ├── run.py                   # Python script to run server
│   ├── run.sh                   # Bash script to run server
│   ├── requirements.txt         # API dependencies
│   └── postman/                 # Postman collections
│       ├── Vhape_Dummy_API.postman_collection.json
│       ├── Vhape_Dummy_API.postman_environment.json
│       └── README.md
│
├── docker/                      # Docker configurations
│   ├── Dockerfile.api_dummy     # API dummy container
│   ├── Dockerfile.bjparser      # Parser/test runner container
│   └── entrypoint.sh            # Container entrypoint script
│
├── docs/                        # Documentation
│   ├── README_vhape.md          # Core framework documentation
│   ├── README_api_dummy.md      # API dummy documentation
│   ├── README_tests_unit.md     # Unit tests documentation
│   ├── README_tests_results.md  # Test results documentation
│   ├── README_project_structure.md  # This file
│   ├── dsl-syntax.md            # DSL syntax guide
│   ├── dsl-keywords-reference.md # DSL keywords reference
│
├── features/                    # BDD feature files (Gherkin)
│   ├── api_security.feature     # API security scenarios
│   ├── auth.feature             # Authentication scenarios
│   ├── edge_cases.feature       # Edge case scenarios
│   ├── failure_scenarios.feature # Failure test scenarios
│   ├── workflow.feature         # Workflow scenarios
│   └── steps/                   # Step definitions
│       ├── __init__.py
│       ├── auth_steps.py        # Given/When/Then implementations
│       └── environment.py       # Behave hooks and setup
│
├── tests/                       # Test suite
│   ├── e2e/                     # End-to-end tests
│   │   ├── html_report_generator.py  # HTML report generator
│   │   └── run_e2e_tests.py     # E2E test runner
│   ├── results/                 # Test execution reports
│   │   ├── summary_*.json       # JSON reports
│   │   └── summary_*.html       # HTML reports
│   └── unit/                    # Unit tests
│       ├── test_auth_steps.py   # Auth steps tests
│       ├── test_parser.py       # Parser tests
│       └── test_summary.py      # Reporting tests
│
├── vhape/                       # Core framework
│   ├── __init__.py              # Module initialization
│   ├── behave.ini               # Behave configuration
│   ├── parser/                  # DSL Parser
│   │   ├── __init__.py          # Exports: StepParser, parse_step, DSLParseError
│   │   ├── grammar.lark         # Lark grammar definition
│   │   └── parse.py             # Parser implementation
│   └── reporting/               # Reporting system
│       ├── __init__.py          # Exports: TestSummary
│       └── summary.py           # TestSummary class
│
├── .gitignore                   # Git ignore rules
├── docker-compose.yml           # Docker Compose configuration
├── env.example                  # Environment variables example
├── LICENSE                      # MIT License
├── README.md                    # Main project documentation
├── requirements.txt             # Main project dependencies
└── requirements-dev.txt         # Development dependencies
```

## Key Directories

### `api_dummy/`
Dummy API server built with FastAPI. Provides controlled endpoints for testing authentication and authorization scenarios.

**Key Files:**
- `main.py` - FastAPI application with test endpoints
- `run.py` / `run.sh` - Server startup scripts
- `postman/` - Postman collections for manual API testing

### `vhape/`
Core framework containing the DSL parser and reporting system.

**Subdirectories:**
- `parser/` - DSL parser using Lark grammar
- `reporting/` - Test summary and report generation

### `features/`
BDD feature files written in Gherkin syntax and step definitions.

**Key Files:**
- `*.feature` - Gherkin scenario files
- `steps/auth_steps.py` - Step implementations using DSL parser
- `steps/environment.py` - Behave hooks for test setup/teardown

### `tests/`
Comprehensive test suite with unit and E2E tests.

**Subdirectories:**
- `unit/` - Unit tests for parser, reporting, and step logic
- `e2e/` - End-to-end test runner and HTML report generator
- `results/` - Generated test reports (JSON and HTML)

### `docs/`
Complete project documentation.

**Key Documents:**
- Framework, API, and testing documentation
- DSL syntax and keywords reference
- Project structure (this document)

### `docker/`
Docker container configurations for containerized execution.

**Key Files:**
- `Dockerfile.api_dummy` - API server container
- `Dockerfile.bjparser` - Test runner container
- `entrypoint.sh` - Container initialization script

## File Types

### Python Files (`.py`)
- **Application code**: `api_dummy/main.py`, `vhape/parser/parse.py`, `vhape/reporting/summary.py`
- **Step definitions**: `features/steps/*.py`
- **Test files**: `tests/unit/*.py`, `tests/e2e/*.py`
- **Module initialization**: `__init__.py` files

### Feature Files (`.feature`)
Gherkin syntax files defining BDD scenarios:
- `auth.feature` - Authentication tests
- `api_security.feature` - Security validation tests
- `workflow.feature` - Workflow scenarios
- `edge_cases.feature` - Edge case testing
- `failure_scenarios.feature` - Failure scenario testing

### Configuration Files
- `docker-compose.yml` - Docker services configuration
- `vhape/behave.ini` - Behave framework configuration
- `requirements.txt` - Python dependencies
- `requirements-dev.txt` - Development dependencies
- `.gitignore` - Git ignore patterns

### Documentation Files (`.md`)
Markdown documentation in `docs/` directory covering all aspects of the project.

## Module Dependencies

```
vhape (core framework)
├── lark-parser          # DSL parsing
└── behave              # BDD framework (indirect)

api_dummy
├── fastapi             # Web framework
└── uvicorn             # ASGI server

tests
├── pytest              # Testing framework
└── pytest-cov          # Coverage reporting
```

## Related Documentation

- **[Vhape Framework](README_vhape.md)** - Core framework details
- **[API Dummy](README_api_dummy.md)** - API documentation
- **[Testing Guide](README_tests_unit.md)** - Test documentation
- **[Main README](../README.md)** - Project overview

