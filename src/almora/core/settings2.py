from typing import Any


class SettingsItem:
    def __init__(self, name: str, space: list | None, default: Any):
        self._name: str = name
        self._space: list | None = space
        self._default: Any = default
        self._value: Any = self._default
        self._preparing: tuple[bool, Any] | None = None

        self.validate_attribute()

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

    def validate_attribute(self) -> bool:
        if self._space:
            if not self._default in self._space:
                raise AttributeError(
                    f"{self._name} > default : {self._default} is not a valid setting. default value must be in ({self._space})")
            if not self._value in self._space:
                raise AttributeError(
                    f"{self._name} : {self._value} is not a valid setting. value must be in ({self._space})")
        return True

    def validate_value(self, value) -> bool:
        if self._space:
            if not value in self._space:
                raise AttributeError(f"{value} is not a valid value. value must be in ({self._space})")
        return True

    def prepare(self, value: Any) -> SettingsItem:
        if self.validate_value(value):
            self._preparing = (True, value)
        else:
            raise AttributeError(f"{value} is not a valid value. value must be in ({self._space})")
        return self

    def unprepare(self):
        self._preparing = None

    def apply(self) -> None:
        if self._preparing:
            valid, value = self._preparing
            if valid:
                self._value = value
            else:
                raise AttributeError(f"{value} is not a valid value. value must be in ({self._space})")
        else:
            raise AttributeError(f"{self._name} have not been prepared.")
        self.unprepare()

    def get_dict(self) -> dict:
        result: dict = {
            "name": self._name,
            "space": self._space,
            "default": self._default,
            "value": self._value
        }
        return result


class Switch(SettingsItem):
    def __init__(self, name: str, default: bool):
        super().__init__(name=name, space=[True, False], default=default)

    def toggle(self):
        self.prepare(not self.value)
        valid, value = self._preparing
        if valid and type(value) is bool:
            return self
        else:
            self.unprepare()
            raise AttributeError(f"{value} is not a valid value. value must be in ({self._space})")


class Selection(SettingsItem):
    def __init__(self, name: str, space: list, default: Any):
        if not type(space) is list:
            raise TypeError(f"Provided space >>>{space}<<< is not a list")
        super().__init__(name=name, space=space, default=default)