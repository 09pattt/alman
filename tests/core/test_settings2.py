import pytest
from almora.core.settings2 import *

@pytest.mark.parametrize("name, space, default", [
    (
        "log_to_file",
        [True, False],
        True
    ),
    (
        "open_on_start",
        [True, False],
        True
    ),
    (
        "log_max_bytes",
        [1, 2, 4, 8, 16],
        4
    ),
    (
        "setting",
        [1, 2, 3, "A", "B"],
        "A"
    ),
    (
        "test",
        None,
        "hello"
    ),
    (
        "test",
        None,
        256
    )
])
def test_setting_item_valid_init(name, space, default):
    item = SettingsItem(name, space, default)
    assert item.name == name
    assert item.space == space
    assert item.default == default
    assert item.value == default


@pytest.mark.parametrize("space, default", [
    (
        [True, False],
        None
    ),
    (
        [1, 2, 4],
        100
    ),
    (
        [1, 2, 3, "A", "B"],
        0
    )
])
def test_setting_item_invalid_init(space, default):
    with pytest.raises(AttributeError):
        SettingsItem("test", space, default)

@pytest.mark.parametrize("valid, space, default, value", [
    (
        True,
        [True, False],
        True,
        False
    ),
    (
        True,
        [1, 2, 4, 8],
        4,
        8
    ),
    (
        True,
        [1, 2, 3, "A", "B"],
        2,
        "A"
    ),
    (
        False,
        [1, 2, 4, "A", "B"],
        2,
        "C"
    ),
    (
        False,
        [1, 2, 4, 8],
        4,
        16
    ),
    (
        True,
        None,
        "user",
        "u s e r"
    ),
    (
        True,
        None,
        "user",
        256
    ),
    (
        True,
        None,
        256,
        3.14
    ),
])
def test_settings_item_set(valid, space, default, value):
    item = SettingsItem("test", space, default)
    if not valid:
        with pytest.raises(AttributeError):
            item.prepare(value)
        return
    prepared_valid, prepared_value = item.prepare(value)._preparing
    assert prepared_valid
    assert prepared_value == value
    item.apply()
    assert item.value == value

@pytest.mark.parametrize("name, space, default, value", [
    (
        "test",
        [True, False],
        True,
        False
    ),
    (
        "log_max_bytes",
        [1,2,4,8],
        4,
        8
    ),
    (
        "test",
        None,
        "user",
        "Patrick"
    ),
])
def test_settings_item_get_dict(name, space, default, value):
    item = SettingsItem(name, space, default)
    item.prepare(value).apply()
    setting_dict = item.get_dict()
    assert setting_dict["name"] == name
    assert setting_dict["space"] == space
    assert setting_dict["default"] == default
    assert setting_dict["value"] == value

@pytest.mark.parametrize("valid, value", [
    (
        True,
        True
    ),
    (
        True,
        0
    ),
    (
        False,
        None
    ),
    (
        False,
        2
    ),
])
def test_switch_setter(valid, value):
    item = Switch("test", True)
    if not valid:
        with pytest.raises(AttributeError):
            item.prepare(value).apply()
        return
    item.prepare(value).apply()
    assert item.value == value
    item.toggle().apply()
    assert item.value is not value

@pytest.mark.parametrize("valid, space, default, value", [
    (
        True,
        [1, 2, 4, 8],
        2,
        4
    ),
    (
        True,
        ['INFO', 'DEBUG', 'WARNING'],
        'INFO',
        'DEBUG'
    ),
    (
        False,
        [1, 2, 4, 8],
        2,
        16
    ),
    (
        False,
        [1, 2, 4, 8],
        2,
        '2'
    )
])
def test_selection_setter(valid, space, default, value):
    item = Selection("test", space, default)
    if not valid:
        with pytest.raises(AttributeError):
            item.prepare(value).apply()
        return
    assert item.value == default
    item.prepare(value).apply()
    assert item.value == value