# Vhape

> **Simplifying API Security Validation for Developers**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Behave](https://img.shields.io/badge/BDD-Behave-orange.svg)](https://behave.readthedocs.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

**Vhape** is a minimalistic framework that enables developers to validate REST API authentication and authorization using a simple Domain-Specific Language (DSL) and Behavior-Driven Development (BDD) principles. Built for developers and startup founders who need to ensure their APIs are secure without deep security expertise.

---

## 🎯 Overview

**Vhape** simplifies API security validation by letting developers write and run security tests in plain English. Using a simple DSL and BDD with Behave, it generates interactive HTML and JSON reports, all running seamlessly in Docker. Perfect for developers, startup founders, and teams needing fast, reliable API security checks.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔤 **Simple DSL** | Write security tests using intuitive phrases instead of complex code |
| 📝 **BDD with Behave** | Structured, readable test scenarios following Gherkin syntax |
| 🎮 **Interactive Runner** | Select and run specific test features with an intuitive menu |
| 📊 **Modern Reports** | Interactive HTML reports with search, filters, and visual statistics |
| 📄 **CI/CD Ready** | JSON reports for seamless integration with continuous integration |
| 🐳 **Docker Support** | Complete containerized setup for easy deployment |
| ✅ **Well Tested** | Comprehensive test suite with 94+ unit tests |

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+

### Run with Docker

```bash
# 1. Clone the repository
git clone https://github.com/Angel-crypt/vhape-mvp.git
cd vhape-mvp

# 2. Build and start services
docker-compose up -d

# 3. Run tests
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --all
```

**Test Flow:**

```text
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ api_dummy   │────────▶│  bjparser   │────────▶│   Reports   │
│  (Port 8000)│  HTTP   │  (Test      │  Test   │  (HTML/JSON)│
│             │ Requests│   Runner)   │ Results │             │
└─────────────┘         └─────────────┘         └─────────────┘
     ▲                          │
     │                          │
     └──────────────────────────┘
        Validates API Security
```

**What happens:**

- `api_dummy` service starts on port `8000` (test API server)
- `bjparser` service runs E2E tests against the API
- HTML and JSON reports are generated in `./tests/results/`

> 📖 **For detailed Docker setup and troubleshooting**, see [`DOCS/README_api_dummy.md`](DOCS/README_api_dummy.md)

### Example Test Scenario

```gherkin
Feature: API Security Validation
  Scenario: Valid token should grant access
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token
```

> 📖 **For complete DSL syntax, keywords, and more examples**, see [`DOCS/dsl-syntax.md`](DOCS/dsl-syntax.md) and [`DOCS/dsl-keywords-reference.md`](DOCS/dsl-keywords-reference.md)

---

## 🛠️ Usage

### Running Tests

```bash
# Interactive mode (select features from menu)
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py

# Run all features
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --all

# Run specific features
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --features auth,api_security

# Direct Behave execution
docker-compose run --rm bjparser behave features/
```

### Viewing Reports

After running tests, reports are available in `./tests/results/`:

- **HTML Reports**: Open `summary_YYYYMMDD_HHMMSS.html` in your browser
- **JSON Reports**: Use `summary_YYYYMMDD_HHMMSS.json` for CI/CD integration

Reports automatically open in your default browser when generated.

### Configuration

Set the API URL via environment variable:

```bash
# In docker-compose.yml or .env file
VHAPE_API_URL=http://api_dummy:8000
```

---

## 🧪 Testing

```bash
# Unit tests
docker-compose run --rm bjparser pytest tests/unit/ -v

# E2E tests
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --all
```

---

## 📚 Documentation

All detailed documentation is available in the [`DOCS/`](DOCS/) directory:

- **[DSL Syntax & Keywords](DOCS/)** - Complete DSL reference, syntax guide, and keyword lookup
- **[Vhape Framework](DOCS/README_vhape.md)** - Core framework, parser architecture, and reporting system
- **[API Dummy](DOCS/README_api_dummy.md)** - Dummy API endpoints, Docker setup, and Postman collections
- **[Testing Guide](DOCS/README_tests_unit.md)** - Unit tests, E2E tests, and test results documentation
- **[Project Structure](DOCS/README_vhape.md#module-structure)** - Detailed project organization

---

## 🤝 Contributing

Contributions are welcome! This project was developed for educational purposes, and we encourage developers to explore, learn, and contribute.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and ensure tests pass
4. **Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **Push to the branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

### Development Setup

For local development without Docker, see the detailed setup instructions in [`DOCS/README_vhape.md`](DOCS/README_vhape.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Developed for the *Data Structures and Compilers* course at Global University
- Built with [Behave](https://behave.readthedocs.io/) for BDD testing
- Uses [Lark](https://github.com/lark-parser/lark) for DSL parsing
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for the dummy API

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Angel-crypt/vhape-mvp/issues)
- **Documentation**: See [`DOCS/`](DOCS/) directory for detailed guides
- **Questions**: Open an issue for questions or suggestions

---

## 💝 Made with ❤️

Made with ❤️ for developers who care about API security.

[⬆ Back to Top](#vhape)
