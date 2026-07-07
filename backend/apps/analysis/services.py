from django.conf import settings

from apps.repositories.models import Repository

from .exceptions import (
    ActiveAnalysisExists,
    RepositoryNotFound,
)
from .models import (
    AnalysisJob,
    AnalysisStatus,
)




class AnalysisService:

    @classmethod
    def start_analysis(cls, user, repository_id):

        repository = cls._get_repository(
            user,
            repository_id,
        )

        active_job = cls._get_active_job(
            repository,
        )

        if active_job:
            raise ActiveAnalysisExists(active_job)

        return cls._create_analysis_job(
            repository,
        )

    @classmethod
    def _get_repository(cls, user, repository_id):

        repository = Repository.objects.filter(
            id=repository_id,
            user=user,
        ).first()

        if repository is None:
            raise RepositoryNotFound(
                "Repository not found."
            )

        return repository

    @classmethod
    def _get_active_job(cls, repository):

        return AnalysisJob.objects.filter(
            repository=repository,
            status__in=[
                AnalysisStatus.PENDING,
                AnalysisStatus.CLONING,
                AnalysisStatus.INDEXING,
                AnalysisStatus.ANALYZING,
                AnalysisStatus.AI_PROCESSING,
            ],
        ).first()

    @classmethod
    def _create_analysis_job(cls, repository):

        return AnalysisJob.objects.create(
            repository=repository,
            status=AnalysisStatus.PENDING,
            branch=repository.default_branch,
            commit_sha="",
            analysis_version=settings.ANALYSIS_ENGINE_VERSION,
        )