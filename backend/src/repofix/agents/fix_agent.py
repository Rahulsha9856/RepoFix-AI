from repofix.agents.llm_client import LLMClient
from repofix.patching.patch_applier import PatchApplier
from repofix.patching.patch_generator import PatchGenerator
from repofix.testing.test_runner import TestRunner
from repofix.validation.validator import FixValidator


class FixAgent:
    def __init__(self) -> None:
        self.llm = LLMClient()
        self.patch_generator = PatchGenerator()
        self.patch_applier = PatchApplier()
        self.test_runner = TestRunner()
        self.validator = FixValidator()

    def run(
        self,
        repository_path: str,
        issue_title: str,
        issue_description: str,
        relevant_files: list[dict[str, str]],
        static_analysis: dict[str, str],
        reasoning: str,
        max_attempts: int = 3,
    ) -> dict:
        attempts = []

        current_reasoning = reasoning

        for attempt in range(1, max_attempts + 1):
            patch = self.patch_generator.generate_patch(
                issue_title=issue_title,
                issue_description=issue_description,
                relevant_files=relevant_files,
                static_analysis=static_analysis,
                reasoning=current_reasoning,
            )

            try:
                self.patch_applier.apply(
                    repository_path,
                    patch,
                )
            except RuntimeError as error:
                attempts.append(
                    {
                        "attempt": attempt,
                        "status": "patch_failed",
                        "patch": patch,
                        "error": str(error),
                    }
                )

                current_reasoning = self.llm.generate(
                    f"""
The generated patch failed to apply.

Issue:
{issue_title}

Patch:
{patch}

Patch application error:
{error}

Explain how the patch should be corrected.
"""
                )

                continue

            test_result = self.test_runner.run_pytest(
                repository_path
            )

            validation = self.validator.validate(
                test_result,
                patch,
            )

            attempts.append(
                {
                    "attempt": attempt,
                    "status": validation["status"],
                    "patch": patch,
                    "test_output": validation["test_output"],
                }
            )

            if validation["status"] == "validated":
                return {
                    "success": True,
                    "attempts": attempts,
                    "final_patch": patch,
                }

            current_reasoning = self.llm.generate(
                f"""
The proposed fix did not pass the tests.

Issue:
{issue_title}

Previous reasoning:
{current_reasoning}

Generated patch:
{patch}

Test output:
{validation["test_output"]}

Analyze the test failure and explain what should be
changed in the next patch.
"""
            )

        return {
            "success": False,
            "attempts": attempts,
            "final_patch": None,
        }