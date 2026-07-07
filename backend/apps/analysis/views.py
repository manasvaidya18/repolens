from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import (
    ActiveAnalysisExists,
    RepositoryNotFound,
)
from .serializers import (
    AnalysisJobSerializer,
    StartAnalysisSerializer,
)
from .services import AnalysisService


class StartAnalysisView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = StartAnalysisSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        try:

            analysis_job = AnalysisService.start_analysis(
                request.user,
                serializer.validated_data["repository_id"],
            )

        except RepositoryNotFound as e:

            return Response(
                {
                    "message": str(e),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except ActiveAnalysisExists as e:

            response_serializer = AnalysisJobSerializer(
                e.analysis_job,
            )

            return Response(
                {
                    "message": "Analysis already in progress.",
                    "analysis_job": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        response_serializer = AnalysisJobSerializer(
            analysis_job,
        )

        return Response(
            {
                "message": "Analysis job created successfully.",
                "analysis_job": response_serializer.data,
            },
            status=status.HTTP_202_ACCEPTED,
        )