from django.db import models

from apps.repositories.models import Repository


class AnalysisStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CLONING = "CLONING", "Cloning"
    INDEXING = "INDEXING", "Indexing"
    ANALYZING = "ANALYZING", "Analyzing"
    AI_PROCESSING = "AI_PROCESSING", "Generating AI Insights"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"


class AnalysisJob(models.Model):

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="analysis_jobs",
    )

    status = models.CharField(
        max_length=20,
        choices=AnalysisStatus.choices,
        default=AnalysisStatus.PENDING,
    )

    branch = models.CharField(
        max_length=255,
    )

    commit_sha = models.CharField(
        max_length=40,
        db_index=True,
    )

    analysis_version = models.CharField(
        max_length=50,
        default="1.0.0",
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.repository.repository_name} "
            f"({self.status})"
        )