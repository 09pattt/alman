from typing import Any


class SettingsItem:
    def __init__(self, name: str, space: list | None, default: Any):
        self._name: str = name
        self._space: list | None = space
        self._default: Any = default
        self._value: Any = self._default
        self._preparing: tuple[bool, Any] | None = None

        self.validate_value(self._default)
        self.validate_value(self._value)

    @property
    def name(self) -> str:
        return self._name

    @property
    def space(self) -> list | None:
        return self._space

    @property
    def default(self) -> Any:
        return self._default

    @property
    def value(self) -> Any:
        return self._value

    def __str__(self) -> str:
        return str(f"{self.name} : {self.value}")

    def validate_value(self, value) -> bool:
        if self.space:
            if not value in self.space:
                raise AttributeError(f"{value} is not a valid value. value must be in ({self.space})")
        return True

    def prepare(self, value: Any) -> None:
        self._preparing = (self.validate_value(value), value)

    def unprepare(self):
        self._preparing = None

    def apply(self) -> None:
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
        result: dict = {
            "name": self.name,
            "space": self.space,
            "default": self.default,
            "value": self.value
        }
        return result


class Switch(SettingsItem):
    def __init__(self, name: str, default: bool):
        super().__init__(name=name, space=[True, False], default=default)

    def toggle(self) -> SettingsItem:
        self.prepare(value = not self.value)
        return self


class Selection(SettingsItem):
    def __init__(self, name: str, space: list, default: Any):
        if not type(space) is list:
            raise TypeError(f"Provided space >>>{space}<<< is not a list")
        super().__init__(name=name, space=space, default=default)

    # Add additional function such as fetching current index for navigation


class SettingsInput(SettingsItem):
    def __init__(self,
                 name: str,
                 default: str | None = None,
                 required: bool = False):
        super().__init__(name=name, space=None, default=default)
        self._required: bool = required

    @property
    def required(self) -> bool:
        return self._required

    def validate_value(self, value) -> bool:
        raise SystemError(f"SettingsInput.validate_value has not been implemented")


class StringSettings(SettingsInput):
    def __init__(self,
                 name: str,
                 default: str | None = None,
                 required: bool = False,
                 max_len: int | None = None,
                 min_len: int | None = None,
                 is_case_sensitive: bool = False):
        super().__init__(name=name,
                         default=default,
                         required=required)
        self._max_len: int | None = max_len
        self._min_len: int | None = min_len
        self._is_case_sensitive: bool = is_case_sensitive

    @property
    def max_len(self) -> int | None:
        return self._max_len

    @property
    def min_len(self) -> int | None:
        return self._min_len

    @property
    def is_case_sensitive(self) -> bool:
        return self._is_case_sensitive

    def validate_value(self, value) -> bool:
        if self.required and not value:
            raise AttributeError(f">>>{self.name}<<< is required")
        if self.max_len and len(value) > self.max_len:
            raise AttributeError(f"{value} is too long")
        if self.min_len and len(value) < self.min_len:
            raise AttributeError(f"{value} is too short")
        return True

    def prepare(self, value: Any) -> None:
        if not self.is_case_sensitive:
            value = value.lower()
        self._preparing = (self.validate_value(value), value)


class IntSettings(SettingsInput):
    def __init__(self,
                 name: str,
                 default: str | None = None,
                 required: bool = False,
                 max_val: int | None = None,
                 min_val: int | None = None):
        super().__init__(name=name,
                         default=default,
                         required=required)
        self._max_val: int | None = max_val
        self._min_val: int | None = min_val

    @property
    def max_val(self) -> int | None:
        return self._max_val

    @property
    def min_val(self) -> int | None:
        return self._min_val

    def validate_value(self, value) -> bool:
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
        self._preparing = (self.validate_value(value), value)
