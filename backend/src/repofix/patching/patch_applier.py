import subprocess
from pathlib import Path


class PatchApplier:
    def apply(self, repository_path: str, patch: str) -> str:
        patch = patch.replace("\r\n", "\n").replace("\r", "\n")

        # Normalize line endings in files referenced by the patch.
        for line in patch.splitlines():
            if line.startswith("+++ b/"):
                relative_path = line[6:].strip()
                target_file = Path(repository_path) / relative_path

                if target_file.is_file():
                    content = target_file.read_text(
                        encoding="utf-8"
                    )
                    target_file.write_text(
                        content.replace("\r\n", "\n").replace("\r", "\n"),
                        encoding="utf-8",
                        newline="\n",
                    )

        result = subprocess.run(
            ["git", "apply", "--whitespace=fix", "-"],
            cwd=repository_path,
            input=patch,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Patch application failed:\n"
                f"{result.stderr}"
                f"\nPatch received by Git:\n{patch!r}"
            )

        return "Patch applied successfully"