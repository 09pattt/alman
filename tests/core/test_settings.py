import pytest
import json
from pathlib import Path
from alman.core.settings import Settings, LoggingSettings, merge_settings
from alman.core.base import *


@pytest.mark.parametrize("expected, template_json, local_json, create_template_file, create_local_file", [
    (
            {"config1":{"option1":2, "option2":False}, "config2":True},
            {"config1":{"option1":3, "option2":False}, "config2":True},
            {"config1":{"option1":2}},
            True,
            True
    ),
    (
            {"config1":{"option1":True, "option2":False, "option3":False}, "configA":{"option1":512}},
            {"config1":{"option1":True, "option2":True, "option3":False}, "configA":{"option1":512}},
            {"config1":{"option1":2, "option2":False}, "config2":True},
            True,
            True
    ),
    (
            {"config1":{"option1":3, "option2":False}, "config2":True},
            {"config1":{"option1":3, "option2":False}, "config2":True},
            None,
            True,
            False
    ),
])
def test_settings_loader_creates_local_from_template(tmp_path, expected, template_json, local_json, create_template_file, create_local_file):
    root = Path(tmp_path)
    template = root / "settings.json.example"
    local = root / "settings.json"

    if create_template_file:
        template.touch()
        template.write_text(json.dumps(template_json))
    if create_local_file:
        local.touch()
        local.write_text(json.dumps(local_json))

    settings = Settings(app_root=root)
    assert settings.settings == expected
    with open(str(local), 'r', encoding="utf-8") as f:
        settings_json = json.load(f)
    assert settings_json == expected


def test_get_logging_settings(tmp_path):
    example_template_settings = {
        "logging" : {
          "log_level" : "INFO",
          "show_path" : True,
          "log_to_file" : True
        }
    }

    example_local_settings = {
        "logging": {
            "log_level": "INFO",
            "show_path": False,
        }
    }

    root = Path(tmp_path)
    template = root / "settings.json.example"
    template.touch()
    template.write_text(json.dumps(example_template_settings))
    local = root / "settings.json"
    local.touch()
    local.write_text(json.dumps(example_local_settings))

    master_settings = Settings(app_root=root)

    with open(str(local), 'r', encoding="utf-8") as f:
        local_settings = json.load(f)

    logging_settings = LoggingSettings(settings=master_settings)
    expected_log_level = local_settings["logging"]["log_level"]
    expected_show_path = local_settings["logging"]["show_path"]
    expected_log_to_file = local_settings["logging"]["log_to_file"]

    assert logging_settings.log_level == expected_log_level
    assert logging_settings.show_path == expected_show_path
    assert logging_settings.log_to_file == expected_log_to_file

def test_merge_settings(tmp_path):
    console.rule(f"TEST-MERGE-SETTINGS")
    example_template_settings = {
        "logging": {
            "log_level": "INFO",
            "show_path": True,
            "log_to_file": True
        }
    }

    expected_local_settings = {
        "logging": {
            "log_level": "DEBUG",
            "show_path": True,
            "log_to_file": False
        }
    }

    root = Path(tmp_path)
    template = root / "settings.json.example"
    template.touch()
    template.write_text(json.dumps(example_template_settings))
    local = root / "settings.json"

    master_settings = Settings(app_root=root)

    logging_settings = LoggingSettings(master_settings)
    logging_settings.log_level = "DEBUG"
    logging_settings.log_to_file = False
    master_settings.settings = merge_settings(master=master_settings, branch=logging_settings)
    master_settings.save_settings()

    with open(str(local), 'r', encoding="utf-8") as f:
        local_settings = json.load(f)

    console.print(local_settings)

    assert master_settings.settings == expected_local_settings