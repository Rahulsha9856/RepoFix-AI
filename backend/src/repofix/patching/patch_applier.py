
import subprocess
from pathlib import Path


class PatchApplier:
    def apply(self, repository_path: str, patch: str) -> str:
        repository = Path(repository_path)

        patch = patch.replace("\r\n", "\n").replace("\r", "\n")
        patch = patch.strip() + "\n"

        result = subprocess.run(
            [
                "git",
                "-c", "core.autocrlf=false",
                "apply",
                "--ignore-whitespace",
                "--whitespace=nowarn",
                "-",
            ],
            cwd=str(repository),
            input=patch,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode != 0:
            error_message = result.stderr or result.stdout
            raise RuntimeError(
                f"Patch application failed:\n{error_message}\n\n"
                f"Patch received by Git:\n{patch}"
            )

        return "Patch applied successfully"
