import subprocess


class TestRunner:
    def run_pytest(self, repository_path: str) -> dict[str, object]:
        result = subprocess.run(
            ["pytest", "-q"],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "output": result.stdout + result.stderr,
        }