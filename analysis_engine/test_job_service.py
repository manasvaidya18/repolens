import asyncio

from app.database import AsyncSessionLocal
from services.job_service import JobService


async def main():

    async with AsyncSessionLocal() as session:

        job = await JobService.claim_next_job(session)

        if job is None:
            print("No pending jobs found.")
            return

        print("Job claimed successfully.")
        print("Job ID:", job.id)
        print("Status:", job.status)
        print("Started at:", job.started_at)

        print("\nRepository:")
        print("GitHub ID:", job.repository.github_repo_id)
        print("Owner:", job.repository.github_owner)
        print("Name:", job.repository.repository_name)
        print("Default branch:", job.repository.default_branch)


if __name__ == "__main__":
    asyncio.run(main())