# Development Setup Guide

This guide walks through setting up your development environment and running unit tests for Almora.

---

## Prerequisites

* Python 3.14+
* Virtual Environment manager (`venv`)

---

## Environment Setup

1. **Clone & Navigate to Workspace**:
   ```bash
   cd /Path/to/your_workspace
   ```

2. **Activate Virtual Environment**:
   ```bash
   source .venv_dev/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -e .[dev]
   ```

---

## Running Tests

Run the full pytest suite:
```bash
.venv_dev/bin/pytest
```

Run specific test modules:
```bash
.venv_dev/bin/pytest tests/core/test_settings.py
```
