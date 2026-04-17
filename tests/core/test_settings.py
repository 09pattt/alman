import pytest
import json
from pathlib import Path
from alman.core.settings import Settings

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
    app_root = Path(tmp_path)
    template = app_root / "settings.json.example"
    local = app_root / "settings.json"

    if create_template_file:
        template.touch()
        template.write_text(json.dumps(template_json))
    if create_local_file:
        local.touch()
        local.write_text(json.dumps(local_json))

    settings = Settings(app_root=app_root)
    assert settings.settings == expected
    with open(str(local), 'r', encoding="utf-8") as f:
        settings_json = json.load(f)
    assert settings_json == expected