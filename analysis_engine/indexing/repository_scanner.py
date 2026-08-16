from pathlib import Path

from services.git_manager import GitManager

from .exceptions import RepositoryIntegrityError
from .models import FileMetadata, RepositoryIndex


class RepositoryScanner:

    @classmethod
    def scan(
        cls,
        root_path: Path,
    ) -> RepositoryIndex:

        resolved_root = root_path.resolve()

        tracked_files = GitManager.get_tracked_files(
            root_path
        )

        files: list[FileMetadata] = []

        for relative_path in tracked_files:

            absolute_path = root_path / relative_path

            if absolute_path.is_symlink():
                continue

            resolved_file = absolute_path.resolve()

            if not resolved_file.is_relative_to(resolved_root):
                raise RepositoryIntegrityError(
                    f"Tracked file escapes repository boundary: "
                    f"{relative_path}"
                )

            if not absolute_path.exists():
                raise RepositoryIntegrityError(
                    f"Tracked file is missing from working tree: "
                    f"{relative_path}"
                )

            if not absolute_path.is_file():
                raise RepositoryIntegrityError(
                    f"Tracked path is not a regular file: "
                    f"{relative_path}"
                )

            files.append(
                FileMetadata(
                    relative_path=relative_path,
                    extension=relative_path.suffix.lower(),
                    size_bytes=absolute_path.stat().st_size,
                )
            )

        total_size_bytes = sum(
            file.size_bytes
            for file in files
        )

        return RepositoryIndex(
            root_path=resolved_root,
            files=tuple(files),
            total_files=len(files),
            total_size_bytes=total_size_bytes,
        )