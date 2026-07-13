from pathlib import Path
import subprocess

from .exceptions import (
    DirtyRepositoryError,
    GitCommandFailed,
    InvalidRepositoryPath,
)


class GitManager:

    @classmethod
    def clone(
        cls,
        repo_url: str,
        local_path: Path,
    ) -> None:

        cls._run_git_command(
            None,
            "clone",
            repo_url,
            str(local_path),
        )

    @classmethod
    def fetch(
        cls,
        local_path: Path,
    ) -> None:

        cls._run_git_command(
            local_path,
            "fetch",
        )

    @classmethod
    def checkout(
        cls,
        local_path: Path,
        branch: str,
    ) -> None:

        cls._run_git_command(
            local_path,
            "checkout",
            branch,
        )

    @classmethod
    def pull(
    cls,
    local_path: Path,
    branch: str,
    ) -> None:

        cls._run_git_command(
        local_path,
        "pull",
        "origin",
        branch,
        )
    @classmethod
    def repository_exists(
        cls,
        local_path: Path,
    ) -> bool:

        return (
            local_path.exists()
            and
            (local_path / ".git").exists()
        )
    @classmethod
    def is_dirty(
    cls,
    local_path: Path,
        ) -> bool:

        output = cls._run_git_command(
        local_path,
        "status",
        "--porcelain",
        )

        return bool(output)
    @classmethod
    def get_current_commit(
        cls,
        local_path: Path,
    ) -> str:

        return cls._run_git_command(
            local_path,
            "rev-parse",
            "HEAD",
        )
    @classmethod
    def prepare_repository(
    cls,
    repo_url: str,
    local_path: Path,
    branch: str,
    ) -> None:

        if not local_path.exists():
            cls.clone(
            repo_url,
            local_path,
            )

        else:
            if not cls.repository_exists(local_path):
                raise InvalidRepositoryPath(
                f"Path exists but is not a Git repository: {local_path}"
                )

            if cls.is_dirty(local_path):
                raise DirtyRepositoryError(
                f"Repository contains uncommitted changes: {local_path}"
                )

            cls.fetch(local_path)

        cls.checkout(
        local_path,
        branch,
        )

        cls.pull(
        local_path,
        branch,
        )
    @classmethod
    def _run_git_command(
        cls,
        cwd: Path | None,
        *arguments: str,
    ) -> str:

        command = ["git", *arguments]

        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )

        if result.returncode != 0:
            raise GitCommandFailed(
                command=" ".join(command),
                return_code=result.returncode,
                stderr=result.stderr,
            )

        return result.stdout.strip()
    