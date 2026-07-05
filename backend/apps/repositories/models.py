from django.conf import settings
from django.db import models


class Repository(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="repositories",
    )

    github_repo_id = models.BigIntegerField()

    github_owner = models.CharField(max_length=255)

    repository_name = models.CharField(max_length=255)

    default_branch = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "github_repo_id"],
                name="unique_user_repository",
            )
        ]

    def __str__(self):
        return f"{self.github_owner}/{self.repository_name}"