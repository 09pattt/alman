import json
import shutil
import copy
from pathlib import Path
from alman.infrastructure.app_file import root
from alman.utils.data_utils import sync_dictionaries

class Settings:
    def __init__(self,
                 relative_settings_example_path: Path = Path('settings.json.example'),
                 relative_settings_path: Path = Path('settings.json'),
                 app_root: Path = root) -> None:

        self.settings = None
        self.local = app_root / relative_settings_path
        self.template = app_root / relative_settings_example_path

        self.load_settings()

    def restore_settings(self) -> None:
        if self.template.exists():
            shutil.copy2(self.template, self.local)
        else:
            raise FileNotFoundError(f"Program unable to find {str(self.template)}")

    def load_settings(self) -> None:
        if not self.local.exists():
            self.restore_settings()

        with open(str(self.local), 'r', encoding='utf-8') as f:
            local = json.load(f)

        original_local = copy.deepcopy(local)

        with open(str(self.template), 'r', encoding='utf-8') as f:
            template = json.load(f)

        self.settings = sync_dictionaries(template=template, target=local, add_new_key=True, remove_current_key=True)

        if self.settings != original_local:
            with open(self.local, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)