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
# Clone and navigate
git clone https://github.com/Angel-crypt/vhape-mvp.git
cd vhape-mvp

# Build and start services
docker-compose up -d

# Run all tests
docker-compose run --rm bjparser python tests/e2e/run_e2e_tests.py --all
```

**Test Execution Flow:**

```text
┌─────────────┐    HTTP     ┌─────────────┐    Test     ┌─────────────┐
│ api_dummy   │────────────▶│  bjparser   │────────────▶│   Reports   │
│  :8000      │  Requests   │  (Runner)   │   Results   │ HTML / JSON │
└─────────────┘             └─────────────┘             └─────────────┘
      ▲                            │
      │                            │
      └────────────────────────────┘
         Security Validation Tests
```

*The `bjparser` service executes BDD scenarios against `api_dummy`, generating interactive reports in `./tests/results/`.*

### Example Test Scenario

```gherkin
Feature: API Security Validation
  Scenario: Valid token should grant access
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token
```

> 📖 **For complete DSL syntax, keywords, and more examples**, see [`docs/dsl-syntax.md`](docs/dsl-syntax.md) and [`docs/dsl-keywords-reference.md`](docs/dsl-keywords-reference.md)

---

## 🛠️ Usage

For detailed usage instructions, including interactive test execution, advanced options, report viewing, configuration, and all available commands, see the complete usage guide in [`docs/README_api_dummy.md`](docs/README_api_dummy.md).

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

All detailed documentation is available in the [`docs/`](docs/) directory:

- **[DSL Syntax & Keywords](docs/)** - Complete DSL reference, syntax guide, and keyword lookup
- **[Vhape Framework](docs/README_vhape.md)** - Core framework, parser architecture, and reporting system
- **[API Dummy](docs/README_api_dummy.md)** - Dummy API endpoints, Docker setup, and Postman collections
- **[Testing Guide](docs/README_tests_unit.md)** - Unit tests, E2E tests, and test results documentation
- **[Project Structure](docs/README_vhape.md#module-structure)** - Detailed project organization

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

For local development without Docker, see the detailed setup instructions in [`docs/README_vhape.md`](docs/README_vhape.md).

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
- **Documentation**: See [`Docs/`](docs/) directory for detailed guides
- **Questions**: Open an issue for questions or suggestions

---

[⬆ Back to Top](#vhape)
