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
- **Clear Reporting:** Get understandable feedback about API security.
- **Modular & Extensible:** Parser, steps, and features are organized for future growth.
---


## Quick Start


Clone the repository:


```bash
git clone https://github.com/Angel-crypt/vhape-mvp.git
```


### Create a Virtual Environment


It is recommended to use a **virtual environment** to isolate dependencies:


```bash
# Navigate to project folder
cd vhape-mvp


# Create a virtual environment (Linux/macOS)
python3 -m venv venv


# On Windows
python -m venv venv


# Activate the virtual environment (Linux/macOS)
source venv/bin/activate


# Activate the virtual environment (Windows)
venv\Scripts\activate
```


### Install MVP Dependencies


```bash
# Install main dependencies for MVP
pip install -r requirements.txt
```


### (Optional) Install Development Dependencies


For testing, code style, and coverage, you can install the development packages:


```bash
pip install -r requirements-dev.txt
```