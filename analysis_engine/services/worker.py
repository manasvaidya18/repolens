from app.config import settings
from app.database import AsyncSessionLocal

from services.git_manager import GitManager
from services.job_service import JobService


class Worker:

    @classmethod
    async def process_next_job(cls) -> bool:

        async with AsyncSessionLocal() as session:

            job = await JobService.claim_next_job(session)

            if job is None:
                return False

            try:
                repository = job.repository

                repo_url = (
                    f"https://github.com/"
                    f"{repository.github_owner}/"
                    f"{repository.repository_name}.git"
                )

                local_path = (
                    settings.storage_root
                    / str(repository.github_repo_id)
                )

                GitManager.prepare_repository(
                    repo_url=repo_url,
                    local_path=local_path,
                    branch=job.branch,
                )

                commit_sha = GitManager.get_current_commit(
                    local_path,
                )

                await JobService.mark_repository_ready(
                    session=session,
                    job=job,
                    commit_sha=commit_sha,
                )

                return True

            except Exception as error:

                await JobService.mark_failed(
                    session=session,
                    job=job,
                    error_message=str(error),
                )

                return False