import pytest
from almora.infrastructure.filesystem import *

@pytest.mark.parametrize("value, expected", [
    (0, FileType.DIR),
    ("dir", FileType.DIR),
    ("0", FileType.DIR),
    ("di", ValueError),
    (1, FileType.FILE),
    (2, FileType.FILE),
    ("file", FileType.FILE),
    ("fi", ValueError),
    (3.14, TypeError),
    (True, TypeError)
])
def test_file_type_parser(value, expected):
    if expected == ValueError:
        with pytest.raises(ValueError):
            FileType.parse(value)
    elif expected == TypeError:
        with pytest.raises(TypeError):
            FileType.parse(value)
    else:
        value = FileType.parse(value)
        assert value is expected

@pytest.mark.parametrize("path, file_type, expected", [
    ('data', FileType.DIR, FileType.DIR),
    (Path('logs'), FileType.DIR, FileType.DIR),
    ("", FileType.DIR, ValueError),
    ("settings.json", FileType.FILE, FileType.FILE),
    (Path("metadata.mtam"), FileType.FILE, FileType.FILE),
    (123, FileType.FILE, TypeError),
])
def test_almora_path(tmp_path, path, file_type, expected):
    if expected == ValueError:
        with pytest.raises(ValueError):
            AlmoraPath(path, file_type)
    elif expected == TypeError:
        with pytest.raises(TypeError):
            AlmoraPath(path, file_type)
    else:
        path = tmp_path / path
        almora_path = AlmoraPath(path, file_type)
        almora_path.ensure_exists()
        assert almora_path.exists()
        assert almora_path.file_type == expected
        if expected == FileType.DIR:
            assert almora_path.is_dir()
        elif expected == FileType.FILE:
            assert almora_path.is_file()

@pytest.mark.parametrize("name, file_type", [
    ("docs", FileType.DIR),
    ("README.md", FileType.FILE),
    ("logs", FileType.DIR),
    ("settings.json.example", FileType.FILE),
])
def test_environment_file(tmp_path, name, file_type):
    root = Path('tmp_path')
    file = EnvironmentFile(root, name, file_type)
    name = Path(name)
    abs_path = root / name
    assert file.root == root
    assert file.rel_path == name
    assert file.path == abs_path
    assert file.abs_path == abs_path
    assert file.file_type == file_type


@pytest.mark.parametrize("name, file_type", [
    ('logs', FileType.DIR),
    ('README.md', FileType.FILE),
    ('data', FileType.DIR),
    ('settings.json.example', FileType.FILE),
])
def test_environment_schema(tmp_path, name, file_type):
    root = Path(tmp_path)
    schema = EnvironmentSchema(root)
    file = None
    if file_type == FileType.DIR:
        file = schema.add_dir(name)
    elif file_type == FileType.FILE:
        file = schema.add_file(name)
    schema.ensure_schema_exists()
    assert Path(file.path).exists()


def test_app_file_system(tmp_path):
    afs = AppFileSystem(tmp_path)
    afs.schema.ensure_schema_exists()
    assert afs.data.path.exists()
    assert afs.logs.path.exists()
    assert afs.settings.path.exists()
    assert afs.environment.path.exists()