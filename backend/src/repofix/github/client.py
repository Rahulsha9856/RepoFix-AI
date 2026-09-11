from github import Github

from repofix.core.config import settings


class GitHubClient:
    def __init__(self) -> None:
        if not settings.github_token:
            raise ValueError("GITHUB_TOKEN is not configured")

        self.client = Github(settings.github_token)

    def get_repository(self, full_name: str):
        return self.client.get_repo(full_name)

    def get_issue(self, full_name: str, issue_number: int):
        repository = self.get_repository(full_name)
        return repository.get_issue(issue_number)