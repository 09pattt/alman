from pathlib import Path
from enum import Enum


class FileType(Enum):
    DIR = 0
    FILE = 1

    @classmethod
    def parse(cls, value: str | int) -> FileType:
        if isinstance(value, str) and type(value) is str:
            value.lower().replace(' ', '')
            if value in ['dir', 'd', 'directory', 'folder', '0']:
                return FileType.DIR
            elif value in ['file', 'files', 'f', '1']:
                return FileType.FILE
            else:
                raise ValueError("Unknown FileType provided")
        elif isinstance(value, int) and type(value) is int:
            if value > 0:
                return FileType.FILE
            else:
                return FileType.DIR
        else:
            raise TypeError("Invalid argument type provided")


class AlmoraPath(Path):
    def __init__(self, name: Path | str,
                 file_type: str | int | FileType):
        if not isinstance(name, Path) and not isinstance(name, str):
            raise TypeError("Path name must be a Path or str")
        if name == "":
            raise ValueError("Path name cannot be an empty string")
        super().__init__(name)
        if not isinstance(file_type, FileType):
            file_type = FileType.parse(file_type)
        self.file_type: FileType = file_type

    def ensure_exists(self) -> AlmoraPath:
        if self.file_type == FileType.DIR:
            self.mkdir(parents=True, exist_ok=True)
        if self.file_type == FileType.FILE:
            self.touch(exist_ok=True)
        return self


def get_root_path() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / 'src').exists() and (parent / 'README.md').exists():
            return parent
    return current.parent.parent.parent.parent


class EnvironmentFile:
    def __init__(self, root: Path, rel_path: Path | str, file_type: FileType):
        self.root = root
        self.rel_path: Path = Path(rel_path)
        self.abs_path: Path = self.root / self.rel_path
        self.file_type: FileType = file_type

    @property
    def path(self) -> Path:
        return self.abs_path


class EnvironmentSchema:
    def __init__(self, root: Path):
        self._root = root
        self.schema_list: list[AlmoraPath] = []

    def add_dir(self, rel_path: Path | str) -> EnvironmentFile:
        directory = EnvironmentFile(root=self._root, rel_path=rel_path, file_type=FileType.DIR)
        almora_path = AlmoraPath(name=directory.path, file_type=directory.file_type)
        self.schema_list.append(almora_path)
        return directory

    def add_file(self, rel_path: Path | str) -> EnvironmentFile:
        file = EnvironmentFile(root=self._root, rel_path=rel_path, file_type=FileType.FILE)
        almora_path = AlmoraPath(name=file.path, file_type=file.file_type)
        self.schema_list.append(almora_path)
        return file

    def ensure_schema_exists(self) -> None:
        for path in self.schema_list:
            path.ensure_exists()


class AppFileSystem:
    def __init__(self, root: Path = get_root_path()):
        self._root = root
        self.schema = EnvironmentSchema(root=self._root)
        self.data = self.schema.add_dir('data')
        self.logs = self.schema.add_dir('logs')
        self.settings = self.schema.add_file('settings.json')
        self.environment = self.schema.add_file('.env')

    @property
    def root(self) -> Path:
        return self._root
