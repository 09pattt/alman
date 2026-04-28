import json
import shutil
import copy
from pathlib import Path
from typing import Any
from almora.utils.data_utils import sync_dictionaries


class Settings:
    def __init__(self,
                 app_root: Path,
                 relative_settings_example_path: Path = Path('settings.json.example'),
                 relative_settings_path: Path = Path('settings.json')) -> None:

        self.local: Path = app_root / relative_settings_path
        self.template: Path = app_root / relative_settings_example_path
        self.settings: dict = {}
        self.load_settings()

    def restore_settings(self) -> None:
        if self.template.exists():
            shutil.copy2(self.template, self.local)
        else:
            raise FileNotFoundError(f"Program unable to find {str(self.template)}")

    def load_settings(self) -> Settings:
        if not self.local.exists():
            self.restore_settings()

        with open(str(self.local), 'r', encoding='utf-8') as f:
            local = json.load(f)

        original_local = copy.deepcopy(local)

        with open(str(self.template), 'r', encoding='utf-8') as f:
            template = json.load(f)

        self.settings = sync_dictionaries(template=template, target=local, add_new_key=True, remove_current_key=True)

        if self.settings != original_local:
            self.save_settings()

        return self

    def is_valid(self) -> bool:
        result: bool = True
        if not LoggingSettings(self).is_valid():
            result = False

        if not result:
            raise AttributeError("Settings is not valid")
        return result

    def save_settings(self) -> None:
        if self.is_valid():
            with open(self.local, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)


def merge_settings(master: Settings, branch: SettingsBranch) -> dict:
    settings_copy: dict = copy.deepcopy(master.settings)
    branch_dict: dict = branch.get_dict()

    branch_layers: list[dict] = []
    for i in range(0, len(branch.dict_index)):
        dict_to_get: list = []
        for j in range(0, (i+1)):
            dict_to_get.append(branch.dict_index[j])
        layer = settings_copy
        for key in dict_to_get:
            layer = layer.get(key, {})
        branch_layers.append(layer)

    new_settings = settings_copy
    new_branch: dict = sync_dictionaries(template=branch_dict,
                                         target=branch_layers[-1],
                                         add_new_key=False,
                                         remove_current_key=False,
                                         override_value=True)
    if len(branch.dict_index) > 1:
        for i in range(1, len(branch.dict_index)):
            new_branch[branch.dict_index[-i]] = new_branch
    new_settings[branch.dict_index[0]] = new_branch

    return new_settings



class SettingsBranch:
    def __init__(self, dict_index: list[str], settings: Settings):
        self.dict_index = dict_index
        self.dict: dict = {}
        self.settings = settings

    def load_branch_settings(self) -> SettingsBranch:
        self.dict = self.settings.settings
        for key in self.dict_index:
            self.dict = self.dict.get(key, {})

        for key, value in self.dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
            elif type(value) == dict:
                pass
            else:
                pass
        return self

    def get_dict(self) -> dict:
        branch_settings = {}
        for key in self.dict.keys():
            if hasattr(self, key):
                branch_settings[key] = getattr(self, key)
        return branch_settings

    def is_valid(self) -> bool:
        return True


class LoggingSettings(SettingsBranch):
    def __init__(self, settings: Settings):
        super().__init__(dict_index=['logging'], settings=settings)

        self.log_level = 'INFO'
        self.show_path = True
        self.log_to_file = True

        self.load_branch_settings()

    def is_valid(self) -> bool:
        if self.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            pass
        elif type(self.log_level) is int:
            pass
        else:
            return False
        if not type(self.show_path) is bool:
            return False
        if not type(self.log_to_file) is bool:
            return False
        return True


class Option:
    def __init__(self, space: list, default: Any = None) -> None:
        self.space = space
        self.default = default
        if not default in self.space:
            self.default = self.space[0]
        self.selected = self.default

    def restore(self):
        self.selected = self.default

class Switch(Option):
    def __init__(self, default: bool) -> None:
        super().__init__([True, False], default=default)

class Selection(Option):
    def __init__(self, space: list, default: Any = None) -> None:
        super().__init__(space=space, default=default)