import subprocess


class StaticAnalyzer:
    def run_ruff(self, repository_path: str) -> str:
        result = subprocess.run(
            [
                "uv",
                "run",
                "ruff",
                "check",
                ".",
            ],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        return result.stdout + result.stderr

    def run_bandit(self, repository_path: str) -> str:
        result = subprocess.run(
            [
                "uv",
                "run",
                "bandit",
                "-r",
                ".",
                "-f",
                "txt",
            ],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        return result.stdout + result.stderr

    def analyze(self, repository_path: str) -> dict[str, str]:
        return {
            "ruff": self.run_ruff(repository_path),
            "bandit": self.run_bandit(repository_path),
        }