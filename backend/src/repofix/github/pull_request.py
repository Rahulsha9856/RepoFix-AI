
from github import GithubException

from repofix.github.client import GitHubClient


class PullRequestService:
    def __init__(self) -> None:
        self.github = GitHubClient()

    def find_open_pull_request(
        self,
        repository_name: str,
        issue_number: int,
        title: str,
    ) -> dict[str, str] | None:

        repository = self.github.get_repository(repository_name)

        issue_marker = f"for GitHub issue #{issue_number}"

        for pull_request in repository.get_pulls(
            state="open",
            base="main",
        ):
            if (
                pull_request.title == title
                and issue_marker in (pull_request.body or "")
            ):
                return {
                    "number": str(pull_request.number),
                    "url": pull_request.html_url,
                    "title": pull_request.title,
                    "branch": pull_request.head.ref,
                }

        return None

    def create_pull_request(
        self,
        repository_name: str,
        branch_name: str,
        issue_number: int,
        title: str,
        body: str,
    ) -> dict[str, str]:

        existing = self.find_open_pull_request(
            repository_name,
            issue_number,
            title,
        )

        if existing:
            return existing

        repository = self.github.get_repository(repository_name)

        try:
            pull_request = repository.create_pull(
                title=title,
                body=body,
                head=branch_name,
                base="main",
            )

        except GithubException as error:
            if error.status == 422:
                existing = self.find_open_pull_request(
                    repository_name,
                    issue_number,
                    title,
                )

                if existing:
                    return existing

            raise

        return {
            "number": str(pull_request.number),
            "url": pull_request.html_url,
            "title": pull_request.title,
            "branch": pull_request.head.ref,
        }
