from pathlib import Path

from repofix.retrieval.file_scanner import FileScanner


class RepositoryIndexer:
    def build_index(self, repository_path: str) -> list[dict[str, str]]:
        root = Path(repository_path)

        scanner = FileScanner()
        files = scanner.scan_repository(repository_path)

        index: list[dict[str, str]] = []

        for relative_path in files:
            file_path = root / relative_path

            try:
                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except OSError:
                continue

            index.append(
                {
                    "path": relative_path,
                    "content": content,
                }
            )

        return index