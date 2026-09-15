from repofix.github.client import GitHubClient


class PullRequestService:
    def __init__(self) -> None:
        self.github = GitHubClient()

    def create_pull_request(
        self,
        repository_name: str,
        branch_name: str,
        issue_number: int,
        title: str,
        body: str,
    ) -> dict[str, str]:
        repository = self.github.get_repository(
            repository_name
        )

        pull_request = repository.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base="main",
        )

        return {
            "number": str(pull_request.number),
            "url": pull_request.html_url,
            "title": pull_request.title,
        }