from pathlib import Path

from services.git_manager import GitManager


GitManager.prepare_repository(
    repo_url="https://github.com/example/example.git",
    local_path=Path("storage/repositories/fake"),
    branch="main",
)