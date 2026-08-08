"""Configuration setting item abstractions and input validation models."""

from typing import Any


class SettingsItem:
    """Represents a base configuration setting item with validation and staged update support.

    Attributes:
        name (str): Unique identifier for the setting item.
        space (list | None): List of allowed valid values, or None if unconstrained.
        default (Any): Default value for the setting.
        value (Any): Current active value of the setting.
    """

    def __init__(self, name: str, space: list | None, default: Any):
        """Initialize a SettingsItem instance.

        Args:
            name: The setting identifier.
            space: List of permitted values or None.
            default: The initial default value.

        Raises:
            AttributeError: If default value is not present in space.
        """
        self._name: str = name
        self._space: list | None = space
        self._default: Any = default
        self._value: Any = self._default
        self._preparing: tuple[bool, Any] | None = None

        self.validate_value(self._default)
        self.validate_value(self._value)

    @property
    def name(self) -> str:
        """Get the setting identifier name."""
        return self._name

    @property
    def space(self) -> list | None:
        """Get the domain of valid values allowed for this setting."""
        return self._space

    @property
    def default(self) -> Any:
        """Get the default value of the setting."""
        return self._default

    @property
    def value(self) -> Any:
        """Get the current value of the setting."""
        return self._value

    def __str__(self) -> str:
        """Return a string representation of the setting as 'name : value'."""
        return str(f"{self.name} : {self.value}")

    def validate_value(self, value) -> bool:
        """Validate whether a value falls within the permitted space list.

        Args:
            value: Candidate value to validate.

        Returns:
            bool: True if value is valid.

        Raises:
            AttributeError: If value is not present in self.space.
        """
        if self.space:
            if not value in self.space:
                raise AttributeError(f"{value} is not a valid value. value must be in ({self.space})")
        return True

    def prepare(self, value: Any) -> None:
        """Stage a candidate value for application after validation.

        Args:
            value: Candidate value to stage.
        """
        self._preparing = (self.validate_value(value), value)

    def unprepare(self):
        """Clear any staged candidate value."""
        self._preparing = None

    def apply(self) -> None:
        """Apply the currently staged candidate value to self.value.

        Raises:
            AttributeError: If no candidate value was prepared or if candidate is invalid.
        """
        if self._preparing:
            valid, value = self._preparing
            if valid:
                self._value = value
            else:
                raise AttributeError(f"{value} is not a valid value. value must be in ({self.space})")
        else:
            raise AttributeError(f"{self.name} have not been prepared.")
        self.unprepare()

    def get_dict(self) -> dict:
        """Return a dictionary representation of the setting state.

        Returns:
            dict: Dictionary containing 'name', 'space', 'default', and 'value'.
        """
        result: dict = {
            "name": self.name,
            "space": self.space,
            "default": self.default,
            "value": self.value
        }
        return result


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


class Selection(SettingsItem):
    """Setting item for selecting a choice from a specified list of options."""

    def __init__(self, name: str, space: list, default: Any):
        """Initialize a Selection setting.

        Args:
            name: The setting identifier.
            space: List of selectable options.
            default: The initial default option.

        Raises:
            TypeError: If space is not a list.
        """
        if not type(space) is list:
            raise TypeError(f"Provided space >>>{space}<<< is not a list")
        super().__init__(name=name, space=space, default=default)

    # Add additional function such as fetching current index for navigation


class SettingsInput(SettingsItem):
    """Base setting item for user text or numeric input without a pre-defined value space."""

    def __init__(self,
                 name: str,
                 default: str | None = None,
                 required: bool = False):
        """Initialize a SettingsInput item.

        Args:
            name: The setting identifier.
            default: Default value string or None.
            required: Flag indicating if the input is required.
        """
        super().__init__(name=name, space=None, default=default)
        self._required: bool = required

    @property
    def required(self) -> bool:
        """Get whether input value is required."""
        return self._required

    def validate_value(self, value) -> bool:
        """Abstract validation method for input settings. Must be overridden by subclasses.

        Raises:
            SystemError: Always raised in base class as not implemented.
        """
        raise SystemError(f"SettingsInput.validate_value has not been implemented")


class StringSettings(SettingsInput):
    """Setting item for string input validation (length limits and case sensitivity)."""

    def __init__(self,
                 name: str,
                 default: str | None = None,
                 required: bool = False,
                 max_len: int | None = None,
                 min_len: int | None = None,
                 is_case_sensitive: bool = False):
        """Initialize a StringSettings input item.

        Args:
            name: The setting identifier.
            default: Default string value or None.
            required: Flag indicating if string is required.
            max_len: Maximum permitted length or None.
            min_len: Minimum permitted length or None.
            is_case_sensitive: Whether case should be preserved (False lowercases inputs).
        """
        super().__init__(name=name,
                         default=default,
                         required=required)
        self._max_len: int | None = max_len
        self._min_len: int | None = min_len
        self._is_case_sensitive: bool = is_case_sensitive

    @property
    def max_len(self) -> int | None:
        """Get maximum length restriction."""
        return self._max_len

    @property
    def min_len(self) -> int | None:
        """Get minimum length restriction."""
        return self._min_len

    @property
    def is_case_sensitive(self) -> bool:
        """Get whether input string is case-sensitive."""
        return self._is_case_sensitive

    def validate_value(self, value) -> bool:
        """Validate string value against presence and min/max length constraints.

        Args:
            value: Candidate string value.

        Returns:
            bool: True if valid.

        Raises:
            AttributeError: If required value is missing, or string violates length limits.
        """
        if self.required and not value:
            raise AttributeError(f">>>{self.name}<<< is required")
        if self.max_len and len(value) > self.max_len:
            raise AttributeError(f"{value} is too long")
        if self.min_len and len(value) < self.min_len:
            raise AttributeError(f"{value} is too short")
        return True

    def prepare(self, value: Any) -> None:
        """Stage candidate string value, converting to lowercase if case-insensitive.

        Args:
            value: Candidate string value to stage.
        """
        if not self.is_case_sensitive:
            value = value.lower()
        self._preparing = (self.validate_value(value), value)


class IntSettings(SettingsInput):
    """Setting item for integer input validation (range bounds max_val/min_val)."""

    def __init__(self,
                 name: str,
                 default: str | None = None,
                 required: bool = False,
                 max_val: int | None = None,
                 min_val: int | None = None):
        """Initialize an IntSettings input item.

        Args:
            name: The setting identifier.
            default: Default value or None.
            required: Flag indicating if integer is required.
            max_val: Maximum allowed integer value or None.
            min_val: Minimum allowed integer value or None.
        """
        super().__init__(name=name,
                         default=default,
                         required=required)
        self._max_val: int | None = max_val
        self._min_val: int | None = min_val

    @property
    def max_val(self) -> int | None:
        """Get maximum integer value bound."""
        return self._max_val

    @property
    def min_val(self) -> int | None:
        """Get minimum integer value bound."""
        return self._min_val

    def validate_value(self, value) -> bool:
        """Validate integer value against presence and min/max bounds.

        Args:
            value: Candidate integer value.

        Returns:
            bool: True if valid.

        Raises:
            AttributeError: If required value is missing, or value exceeds min/max bounds.
        """
        if self.required and not value:
            raise AttributeError(f">>>{self.name}<<< is required")
        if self.max_val is not None:
            if value > self.max_val:
                raise AttributeError(f"{value} reached maximum value")
        if self.min_val is not None:
            if value < self.min_val:
                raise AttributeError(f"{value} does not reached minimum value")
        return True

    def prepare(self, value: Any) -> None:
        """Stage candidate integer value after validation.

        Args:
            value: Candidate integer value to stage.
        """
        self._preparing = (self.validate_value(value), value)
