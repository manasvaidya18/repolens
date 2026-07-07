from rest_framework import serializers

from .models import AnalysisJob


class StartAnalysisSerializer(serializers.Serializer):
    repository_id = serializers.IntegerField(min_value=1)


class AnalysisJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalysisJob
        fields = (
            "id",
            "status",
            "branch",
            "commit_sha",
            "analysis_version",
            "created_at",
        )