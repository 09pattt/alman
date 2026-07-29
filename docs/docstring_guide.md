# Almora Python Docstring Style Guide

This document defines the docstring standard for the **Almora** codebase. All new and modified Python code must adhere to the **Google Python Docstring Style**.

---

## 1. General Principles

* **Style**: Use [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) format.
* **Delimiters**: Always enclose docstrings in triple double-quotes (`"""`).
* **Tone**: Use imperative mood for single-line summaries ("Return the value" rather than "Returns the value").
* **Type Annotations**: Prefer native Python type hints in function signatures; omit redundant type names in `Args:` unless adding clarification.

---

## 2. Docstring Structure by Component

### 2.1 Module Docstrings
Place at the top of every `.py` file before imports.

```python
"""Module for setting items and configuration inputs in Almora.

Provides base abstractions for configuration properties, validation rules,
and staged updates (prepare/apply pattern).
"""

from typing import Any
```

---

### 2.2 Class Docstrings
Place immediately below the `class` definition. List key public attributes under `Attributes:`.

```python
class SettingsItem:
    """Represents a base configuration setting item with validation and staged update support.

    Attributes:
        name (str): Unique identifier for the setting item.
        space (list | None): List of allowed valid values, or None if unconstrained.
        default (Any): Default value for the setting.
        value (Any): Current active value of the setting.
    """
```

---

### 2.3 Method & Function Docstrings
Include sections for `Args:`, `Returns:`, and `Raises:` when applicable.

```python
    def validate_value(self, value: Any) -> bool:
        """Validate whether a value falls within the permitted space list.

        Args:
            value: Candidate value to validate.

        Returns:
            bool: True if value is valid.

        Raises:
            AttributeError: If value is not present in self.space.
        """
        if self.space and value not in self.space:
            raise AttributeError(f"{value} is not a valid value. Must be in ({self.space})")
        return True
```

---

### 2.4 Property Docstrings
Property getters require concise summary docstrings describing what the property returns.

```python
    @property
    def name(self) -> str:
        """Get the setting identifier name."""
        return self._name
```

---

## 3. Real Example (`src/almora/core/settings2.py`)

Here is an extract showing the standard in practice:

```python
class Switch(SettingsItem):
    """Setting item for boolean switch configurations (space=[True, False])."""

    def __init__(self, name: str, default: bool):
        """Initialize a boolean Switch setting.

        Args:
            name: The setting identifier.
            default: Initial boolean value.
        """
        super().__init__(name=name, space=[True, False], default=default)

    def toggle(self) -> SettingsItem:
        """Stage the opposite of the current boolean value.

        Returns:
            SettingsItem: self instance for method chaining.
        """
        self.prepare(value=not self.value)
        return self
```
