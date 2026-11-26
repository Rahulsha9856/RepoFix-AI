
import re
import subprocess
from pathlib import Path


class TestRunner:
    def run_pytest(
        self,
        repository_path: str,
        patch: str | None = None,
    ) -> dict[str, object]:

        repository = Path(repository_path)
        test_files = []

        if patch:
            changed_files = re.findall(
                r"^\+\+\+ b/(.+)$",
                patch,
                re.MULTILINE,
            )

            for changed_file in changed_files:
                source_path = Path(changed_file)
                module_name = source_path.stem

                candidates = [
                    repository / source_path.parent / f"test_{module_name}.py",
                    repository / source_path.parent / f"{module_name}_test.py",
                ]

                for candidate in candidates:
                    if candidate.is_file():
                        test_files.append(
                            candidate.relative_to(repository).as_posix()
                        )
                        break

        command = ["pytest", "-q"]

        if test_files:
            command.extend(test_files)

        result = subprocess.run(
            command,
            cwd=str(repository),
            capture_output=True,
            text=True,
        )

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "output": result.stdout + result.stderr,
            "test_files": test_files,
        }
