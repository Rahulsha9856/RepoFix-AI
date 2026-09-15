import subprocess


class PatchApplier:
    def apply(self, repository_path: str, patch: str) -> str:
        result = subprocess.run(
            ["git", "apply", "--whitespace=fix", "-"],
            cwd=repository_path,
            input=patch,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Patch application failed:\n"
                f"{result.stderr}"
            )

        return "Patch applied successfully"