from urllib.parse import urlparse

from rest_framework import serializers

from .models import Repository


class RepositoryImportSerializer(serializers.Serializer):

    github_url = serializers.URLField()

    def validate_github_url(self, value):
        parsed = urlparse(value)

        if parsed.netloc not in ("github.com", "www.github.com"):
            raise serializers.ValidationError(
                "Only GitHub repository URLs are allowed."
            )

        path = parsed.path.strip("/")

        parts = path.split("/")

        if len(parts) != 2:
            raise serializers.ValidationError(
                "URL must be in the format: "
                "https://github.com/<owner>/<repository>"
            )

        return value


class RepositorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Repository

        fields = (
            "id",
            "github_repo_id",
            "github_owner",
            "repository_name",
            "default_branch",
            "created_at",
        )