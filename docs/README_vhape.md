# Vhape Framework

The main Vhape framework that provides the DSL parser and reporting system for API security validation.

## Purpose

This module contains the core of the Vhape framework:

1. **DSL Parser** (`vhape/parser/`): Interprets Gherkin steps written in the Vhape DSL
2. **Reporting System** (`vhape/reporting/`): Generates structured reports of test execution

## Module Structure

```
vhape/
├── parser/              # DSL Parser
│   ├── grammar.lark     # Lark grammar for DSL
│   ├── parse.py         # Parser implementation
│   └── __init__.py      # Exports StepParser, parse_step, DSLParseError
│
├── reporting/           # Reporting system
│   ├── summary.py       # TestSummary class for reports
│   └── __init__.py      # Exports TestSummary
│
├── behave.ini           # Behave configuration file
└── __init__.py          # Module initialization
```

## DSL Parser (`vhape/parser`)

### Functionality

The parser interprets Gherkin steps written in the Vhape DSL and converts them into data structures that can be processed by Behave step definitions.

### Usage

```python
from vhape.parser import parse_step, DSLParseError

# Parse a Given step
result = parse_step("Given I have a valid token")
# {'type': 'given', 'token_type': 'valid'}

# Parse a When step
result = parse_step('When I send a request to "/api/users/me"')
# {'type': 'when', 'endpoint': '/api/users/me'}

# Parse a Then step
result = parse_step("Then the response should validate token")
# {'type': 'then', 'validation': 'validate_token'}
```

### Features

- **Case-insensitive**: Accepts uppercase and lowercase
- **Error handling**: Raises `DSLParseError` for invalid steps
- **Clear structure**: Returns dictionaries with consistent structure
- **Extensible**: Easy to extend with new keywords

### Grammar

The grammar is defined in `grammar.lark` using Lark syntax. It supports:

- **Given steps**: Tokens (valid, admin, user, invalid, none)
- **When steps**: Endpoints in quotes
- **Then steps**: Validations (validate_token, expect_401, access_denied, access_allowed)

## Reporting System (`vhape/reporting`)

### Functionality

The reporting system collects information about test execution and generates structured reports in JSON format.

### Usage

```python
from vhape.reporting import TestSummary

# Create summary instance
summary = TestSummary()

# Add results
summary.add_feature("API Authentication", "passed")
summary.add_scenario("Valid token test", "passed", "API Authentication")
summary.add_step("Given I have a valid token", "passed")

# Finalize and generate report
summary.finalize()
summary.print_summary()  # Display in console
json_file = summary.save_json()  # Save JSON
```

### Features

- **Complete tracking**: Features, scenarios, steps, and security issues
- **Statistics**: Calculates success rate, duration, totals
- **JSON reports**: Generates structured reports for CI/CD
- **Security issues**: Identifies and reports security problems

### Report Format

```json
{
  "start_time": "2025-11-04T13:18:23.123456",
  "end_time": "2025-11-04T13:18:24.567890",
  "statistics": {
    "features": {"total": 4, "passed": 4, "failed": 0},
    "scenarios": {"total": 28, "passed": 28, "failed": 0},
    "steps": {"total": 84, "passed": 84, "failed": 0},
    "security_issues": 0,
    "duration": 1.47,
    "success_rate": 100.0
  },
  "features": [...],
  "scenarios": [...],
  "security_issues": []
}
```

## Integration with Behave

The framework is designed to integrate with Behave:

1. **Step Definitions** (`features/steps/auth_steps.py`) use the parser to interpret steps
2. **Environment Hooks** (`features/steps/environment.py`) use TestSummary to generate reports
3. **Feature Files** (`features/*.feature`) contain scenarios written in DSL

## Dependencies

- `lark-parser==0.12.0` - For DSL parser
- `behave==1.3.3` - BDD framework (indirect dependency)

## Extensibility

The framework is designed to be extensible:

- **New keywords**: Add rules in `grammar.lark` and handling in `parse.py`
- **New report types**: Extend `TestSummary` or create new formatters
- **New validators**: Add new validation types in step definitions

## Testing

Parser unit tests are in `tests/unit/test_parser.py`:

```bash
# Run parser tests
python tests/unit/test_parser.py
# or
pytest tests/unit/test_parser.py -v
```

## Related Documentation

- [`docs/dsl-syntax.md`](../docs/dsl-syntax.md) - Complete DSL syntax guide
- [`docs/dsl-keywords-reference.md`](../docs/dsl-keywords-reference.md) - Quick keyword reference
- [`README.md`](../README.md) - Main project documentation
