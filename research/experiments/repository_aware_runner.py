import json
import sys
from datetime import datetime, timezone
from pathlib import Path


# Add backend/src to Python path
BACKEND_SRC = (
    Path(__file__).resolve().parents[2]
    / "backend"
    / "src"
)

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))


from repofix.agents.llm_client import LLMClient


RESULTS_DIR = (
    Path(__file__).resolve().parents[1]
    / "results"
)


def read_repository_context(
    repository_path: str,
) -> str:

    calculator_file = (
        Path(repository_path)
        / "demo_bug"
        / "calculator.py"
    )

    if calculator_file.exists():
        return calculator_file.read_text(
            encoding="utf-8"
        )

    return ""


def run_condition_b(
    issue_id: int,
    repository_path: str,
) -> dict:
    """
    Condition B:
    Repository-Aware LLM

    Pipeline:
    GitHub issue -> repository retrieval -> LLM -> patch
    """

    repository_context = (
        read_repository_context(
            repository_path
        )
    )

    llm = LLMClient()

    prompt = f"""
You are fixing a GitHub issue.

Issue title:
Fix calculator addition bug

Issue description:
The add function in demo_bug/calculator.py is incorrect.
It should return the sum of a and b.

Repository context:

{repository_context}

Generate a unified Git diff.

Return only the patch.
"""

    patch = llm.generate(prompt)

    result = {
        "experiment": "RepoFix AI Reliability Evaluation",
        "condition": "B",
        "condition_name": "Repository-Aware LLM",
        "issue_id": issue_id,
        "success": bool(patch.strip()),
        "issue_resolved": False,
        "patch_accepted": False,
        "tests_passed": False,
        "incorrect_modification": False,
        "retry_count": 0,
        "localized_files": [],
        "patch": patch,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    for line in patch.splitlines():
        if line.startswith("+++ b/"):
            result["localized_files"].append(
                line[6:]
            )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    result_path = (
        RESULTS_DIR
        / f"condition_B_issue_{issue_id}.json"
    )

    with result_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            result,
            file,
            indent=2,
        )

    return result


if __name__ == "__main__":

    result = run_condition_b(
        issue_id=3,
        repository_path=(
            r"C:\Users\Rahul\RepoFix-AI\workspace\issue-3-8089e4e8"
        ),
    )

    print(
        json.dumps(
            result,
            indent=2,
        )
    )