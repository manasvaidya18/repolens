from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileMetadata:
    relative_path: Path
    extension: str
    size_bytes: int


@dataclass(frozen=True)
class RepositoryIndex:
    root_path: Path
    files: tuple[FileMetadata, ...]
    total_files: int
    total_size_bytes: int