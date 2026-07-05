import requests
from urllib.parse import urlparse

from django.db import IntegrityError

from .models import Repository


class RepositoryNotFound(Exception):
    pass


class RepositoryPrivate(Exception):
    pass


class GitHubTimeout(Exception):
    pass


class GitHubRateLimit(Exception):
    pass


class GitHubServerError(Exception):
    pass


class GitHubConnectionError(Exception):
    pass


class GitHubRequestError(Exception):
    pass


class UnexpectedGitHubResponse(Exception):
    pass


class GitHubService:

    GITHUB_API_BASE_URL = "https://api.github.com"

    @staticmethod
    def import_repository(user, github_url):
        github_owner, repository_name = (
            GitHubService._parse_repository_url(github_url)
        )

        repository_data = GitHubService._fetch_repository(
            github_owner,
            repository_name,
        )

        existing_repository = GitHubService._check_duplicate(
            user,
            repository_data["github_repo_id"],
        )

        if existing_repository:
            return existing_repository, False

        repository = GitHubService._save_repository(
            user,
            repository_data,
        )

        return repository, True

    @staticmethod
    def _parse_repository_url(github_url):
        parsed = urlparse(github_url)

        path = parsed.path.strip("/")

        github_owner, repository_name = path.split("/")

        return github_owner, repository_name

    @staticmethod
    def _fetch_repository(github_owner, repository_name):

        api_url = (
            f"{GitHubService.GITHUB_API_BASE_URL}/repos/"
            f"{github_owner}/{repository_name}"
        )

        try:
            response = requests.get(
                api_url,
                timeout=10,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "GitHub-Analyzer",
                },
            )

        except requests.exceptions.Timeout:
            raise GitHubTimeout()

        except requests.exceptions.ConnectionError:
            raise GitHubConnectionError()

        except requests.exceptions.RequestException:
            raise GitHubRequestError()

        if response.status_code == 404:
            raise RepositoryNotFound()

        if response.status_code == 403:

            data = response.json()

            message = data.get("message", "").lower()

            if "rate limit" in message:
                raise GitHubRateLimit()

            raise RepositoryPrivate()

        if response.status_code >= 500:
            raise GitHubServerError()

        if response.status_code != 200:
            raise UnexpectedGitHubResponse()

        data = response.json()

        return {
            "github_repo_id": data["id"],
            "github_owner": data["owner"]["login"],
            "repository_name": data["name"],
            "default_branch": data["default_branch"],
        }

    @staticmethod
    def _check_duplicate(user, github_repo_id):
        return Repository.objects.filter(
            user=user,
            github_repo_id=github_repo_id,
        ).first()

    @staticmethod
    def _save_repository(user, repository_data):

        try:
            repository = Repository.objects.create(
                user=user,
                github_repo_id=repository_data["github_repo_id"],
                github_owner=repository_data["github_owner"],
                repository_name=repository_data["repository_name"],
                default_branch=repository_data["default_branch"],
            )

            return repository

        except IntegrityError:
            return Repository.objects.get(
                user=user,
                github_repo_id=repository_data["github_repo_id"],
            )