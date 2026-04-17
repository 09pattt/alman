from alman.infrastructure.app_file import AppPath
from pathlib import Path

def test_class_app_path():
    app_path = AppPath()
    assert app_path.BASE == Path('/Users/napat/Project/alman')