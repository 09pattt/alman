# Coding Conventions & Guidelines

All code in the Almora project should adhere to the following style and architecture conventions.

---

## 🎨 Python Code Style

* **PEP 8 Compliance**: Follow standard Python naming conventions (`snake_case` for functions/variables, `PascalCase` for classes).
* **Type Annotations**: Provide explicit type hints for function signatures and properties.
* **Docstrings**: All public modules, classes, and methods must have Google-style docstrings (see [Docstring Guide](../docstring_guide.md)).

---

## 🧪 Testing Standards

* Write unit tests for all new functions and class methods.
* Place tests under `tests/` mirroring the `src/almora/` package structure.
* Maintain clean test isolation using `pytest.mark.parametrize` for input variations.
