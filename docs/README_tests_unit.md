# Unit Tests for Vhape MVP

This directory contains comprehensive unit tests for the core components of the Vhape framework.

## Test Coverage

### 1. Parser Tests (`test_parser.py`)

Tests for the DSL parser that interprets Gherkin-style steps.

**Coverage:**

- ✅ Basic step parsing (Given/When/Then)
- ✅ All token types (valid, admin, user, invalid, none)
- ✅ All validation types (validate_token, expect_401, access_denied, access_allowed)
- ✅ Case-insensitive parsing
- ✅ Edge cases (whitespace, special characters, query strings)
- ✅ Error handling (invalid steps, malformed syntax)
- ✅ Parser initialization

**Test Classes:**

- `TestStepParser`: Basic parsing functionality
- `TestParseStepFunction`: Convenience function tests
- `TestParserEdgeCases`: Edge cases and error handling
- `TestParserInitialization`: Parser setup and initialization

**Total Tests:** 30

### 2. TestSummary Tests (`test_summary.py`)

Tests for the reporting system that generates test summaries and JSON reports.

**Coverage:**

- ✅ Initialization
- ✅ Adding features, scenarios, steps, and security issues
- ✅ Statistics calculation (success rates, counts)
- ✅ JSON report generation
- ✅ Console output formatting
- ✅ Edge cases (empty data, missing finalization)

**Test Classes:**

- `TestTestSummary`: All TestSummary functionality

**Total Tests:** 25

### 3. Auth Steps Logic Tests (`test_auth_steps.py`)

Tests for the authentication step logic without making actual HTTP requests.

**Coverage:**

- ✅ Token mapping (valid, admin, user, invalid, none)
- ✅ Header construction (with/without tokens)
- ✅ Validation logic (all validation types)
- ✅ URL construction
- ✅ Response data extraction
- ✅ Error handling and messages
- ✅ Step text parsing

**Test Classes:**

- `TestTokenMapping`: Token mapping logic
- `TestHeaderConstruction`: HTTP header building
- `TestValidationLogic`: Response validation logic
- `TestStepTextParsing`: Step text construction
- `TestURLConstruction`: URL building
- `TestResponseDataExtraction`: Response parsing
- `TestErrorHandling`: Error message formatting

**Total Tests:** 39

## Running Tests

### Run All Unit Tests

```bash
pytest tests/unit/ -v
```

### Run Specific Test File

```bash
pytest tests/unit/test_parser.py -v
pytest tests/unit/test_summary.py -v
pytest tests/unit/test_auth_steps.py -v
```

### Run Specific Test Class

```bash
pytest tests/unit/test_parser.py::TestStepParser -v
```

### Run Specific Test

```bash
pytest tests/unit/test_parser.py::TestStepParser::test_parse_given_valid_token -v
```

### Run with Coverage

```bash
pytest tests/unit/ --cov=vhape --cov-report=html
```

## Test Statistics

- **Total Tests:** 94
- **Test Files:** 3
- **Components Tested:** 3 (Parser, Reporting, Auth Steps Logic)

## Test Philosophy

These unit tests focus on:

1. **Isolation**: Each test is independent and doesn't require external services
2. **Speed**: Fast execution without network calls or file I/O (except for JSON tests)
3. **Coverage**: Testing both happy paths and edge cases
4. **Maintainability**: Clear test names and organization

## Notes

- Tests use mocks where appropriate to avoid external dependencies
- JSON file tests use temporary directories to avoid polluting the project
- Parser tests verify both successful parsing and error handling
- All tests are designed to be deterministic and repeatable
