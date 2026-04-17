from pathlib import Path
from dataclasses import dataclass, field

__all__ = [
    'AppPath'
]

def get_base_path() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / '.env').exists():
            return parent
    return current.parent.parent.parent.parent

@dataclass
class AppPath:
    _base_path: Path | None = field(default_factory=get_base_path)

    @property
    def BASE(self) -> Path:
        return self._base_path