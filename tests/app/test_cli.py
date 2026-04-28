import pytest
from almora.app.cli import get_parser

@pytest.fixture
def parser():
    return get_parser()

@pytest.mark.parametrize("test_input, expected_command, expected_option", [
    ([], "menu", None),
    (["menu"], "menu", None),
    (["info"], "info", None),
    (["info", "status"], "info", "status"),
    (["info", "settings"], "info", "settings"),
    (["info", "user"], "info", "user"),
])
def test_cli_commands(parser, test_input, expected_command, expected_option):
    args = parser.parse_args(test_input)
    assert args.command == expected_command
    if expected_option:
        assert args.option == expected_option

@pytest.mark.parametrize("test_input, expected_value", [
    ([], {"version": False, "yes": False}),
    (["-v"], {"version": True, "yes": False}),
    (["--version"], {"version": True, "yes": False}),
    (["-y"], {"version": False, "yes": True}),
    (["--yes"], {"version": False, "yes": True}),
    (["-v", "-y"], {"version": True, "yes": True}),
])
def test_cli_flags(parser, test_input, expected_value):
    args = parser.parse_args(test_input)
    assert args.version == expected_value["version"]
    assert args.yes == expected_value["yes"]