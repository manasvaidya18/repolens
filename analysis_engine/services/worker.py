from app.config import settings
from app.database import AsyncSessionLocal

from indexing.repository_scanner import RepositoryScanner
from services.git_manager import GitManager
from services.job_service import JobService

import asyncio
import traceback


class Worker:

    @classmethod
    async def process_next_job(cls) -> bool:

        async with AsyncSessionLocal() as session:

            job = await JobService.claim_next_job(session)

            if job is None:
                print("No jobs found")
                return False

            try:
                print(f"Claimed job: {job.id}")

                repository = job.repository

                repo_url = (
                    f"https://github.com/"
                    f"{repository.github_owner}/"
                    f"{repository.repository_name}.git"
                )

                print(f"Repository URL: {repo_url}")

                local_path = (
                    settings.storage_root
                    / str(repository.github_repo_id)
                )

                print(f"Local path: {local_path}")

                GitManager.prepare_repository(
                    repo_url=repo_url,
                    local_path=local_path,
                    branch=job.branch,
                )

                commit_sha = GitManager.get_current_commit(
                    local_path
                )

                await JobService.mark_repository_ready(
                    session=session,
                    job=job,
                    commit_sha=commit_sha,
                )

                print("Repository cloned successfully")

                repository_index = RepositoryScanner.scan(
                    local_path
                )

                print(
                    f"Indexed {len(repository_index.files)} files"
                    if hasattr(repository_index, "files")
                    else "Repository indexed"
                )

                await JobService.mark_indexing_complete(
                    session=session,
                    job=job,
                )

                print(
                    f"Job {job.id} moved to ANALYZING"
                )

                return True

            except Exception as error:

                print("\nWORKER ERROR:")
                traceback.print_exc()

                await JobService.mark_failed(
                    session=session,
                    job=job,
                    error_message=str(error),
                )

                return False


async def main():

    print("Worker started...")

    while True:

        processed = await Worker.process_next_job()

        if processed:
            print("Processed a job")
        else:
            print("Waiting for jobs...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())