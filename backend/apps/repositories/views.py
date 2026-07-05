from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RepositoryImportSerializer,
    RepositorySerializer,
)
from .services import (
    GitHubService,
    RepositoryNotFound,
    RepositoryPrivate,
    GitHubTimeout,
    GitHubRateLimit,
    GitHubServerError,
    GitHubConnectionError,
    GitHubRequestError,
    UnexpectedGitHubResponse,
)


class RepositoryImportView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        serializer = RepositoryImportSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:

            repository, created = (
                GitHubService.import_repository(
                    request.user,
                    serializer.validated_data["github_url"],
                )
            )

        except RepositoryNotFound:
            return Response(
                {"error": "Repository not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except RepositoryPrivate:
            return Response(
                {"error": "Repository is private."},
                status=status.HTTP_403_FORBIDDEN,
            )

        except GitHubRateLimit:
            return Response(
                {
                    "error": (
                        "GitHub API rate limit exceeded."
                    )
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        except GitHubTimeout:
            return Response(
                {"error": "GitHub timed out."},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )

        except GitHubConnectionError:
            return Response(
                {"error": "Unable to connect to GitHub."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except GitHubServerError:
            return Response(
                {"error": "GitHub server error."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except GitHubRequestError:
            return Response(
                {"error": "GitHub request failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except UnexpectedGitHubResponse:
            return Response(
                {"error": "Unexpected GitHub response."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_serializer = RepositorySerializer(
            repository
        )

        return Response(
            {
                "message": (
                    "Repository imported successfully."
                    if created
                    else "Repository already imported."
                ),
                "created": created,
                "repository": response_serializer.data,
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )