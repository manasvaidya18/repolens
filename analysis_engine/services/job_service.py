from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import AnalysisJob


class JobService:

    @classmethod
    async def claim_next_job(
        cls,
        session: AsyncSession,
    ) -> AnalysisJob | None:

        statement = (
            select(AnalysisJob)
            .where(
                AnalysisJob.status == "PENDING"
            )
            .options(
                selectinload(AnalysisJob.repository)
            )
            .order_by(
                AnalysisJob.created_at.asc(),
                AnalysisJob.id.asc(),
            )
            .with_for_update(
                skip_locked=True,
            )
            .limit(1)
        )

        result = await session.execute(statement)

        job = result.scalar_one_or_none()

        if job is None:
            return None

        job.status = "CLONING"
        job.started_at = datetime.now(timezone.utc)

        await session.commit()

        return job

    @classmethod
    async def mark_repository_ready(
        cls,
        session: AsyncSession,
        job: AnalysisJob,
        commit_sha: str,
    ) -> None:

        job.commit_sha = commit_sha
        job.status = "INDEXING"

        await session.commit()

    @classmethod
    async def mark_failed(
        cls,
        session: AsyncSession,
        job: AnalysisJob,
        error_message: str,
    ) -> None:

        job.status = "FAILED"
        job.error_message = error_message
        job.completed_at = datetime.now(timezone.utc)

        await session.commit()