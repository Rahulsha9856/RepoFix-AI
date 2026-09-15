from pathlib import Path

import git

from repofix.models import Repository


class RepositoryService:
    def clone_repository(
        self,
        repository: Repository,
        destination: str,
    ) -> str:
        destination_path = Path(destination)

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        git.Repo.clone_from(
            repository.clone_url,
            destination_path,
        )

        return str(destination_path)

    def create_fix_branch(
        self,
        repository_path: str,
        branch_name: str,
    ) -> str:
        repo = git.Repo(repository_path)

        if repo.is_dirty(untracked_files=True):
            raise RuntimeError(
                "Repository has uncommitted changes"
            )

        repo.git.checkout("-b", branch_name)

        return branch_name
    
    def commit_fix(
        self,
        repository_path: str,
        message: str,
        ) -> str:
        repo = git.Repo(repository_path)

        if not repo.is_dirty(untracked_files=True):
            raise RuntimeError(
                "No changes available to commit"
            )

        repo.git.add(A=True)

        commit = repo.index.commit(message)

        return commit.hexsha
    
    def push_branch(
        self,
        repository_path: str,
        branch_name: str,
    ) -> str:
        repo = git.Repo(repository_path)

        origin = repo.remote("origin")

        origin.push(
            refspec=f"{branch_name}:{branch_name}"
        )

        return branch_name