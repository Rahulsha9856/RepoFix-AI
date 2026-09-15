from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}


class FileScanner:
    def scan_repository(self, repository_path: str) -> list[str]:
        root = Path(repository_path)
        files: list[str] = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if any(
                directory in IGNORED_DIRECTORIES
                for directory in path.parts
            ):
                continue

            files.append(str(path.relative_to(root)))

        return sorted(files)