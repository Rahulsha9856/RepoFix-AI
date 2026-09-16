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


def run_condition_a(
    issue_id: int,
    repository_path: str,
) -> dict:
    """
    Condition A:
    Direct LLM baseline.

    Pipeline:
    GitHub issue -> LLM -> patch
    """

    llm = LLMClient()

    prompt = """
You are fixing a GitHub issue.

Issue title:
Fix calculator addition bug

Issue description:
The add function in demo_bug/calculator.py is incorrect.
It currently subtracts b from a, but it should return
the sum of a and b.

Expected behavior:
add(2, 3) should return 5.

Generate a unified Git diff containing the required fix.

Do not analyze the repository.
Do not retrieve additional files.
Return only the patch.
"""

    patch = llm.generate(prompt)

    result = {
        "experiment": "RepoFix AI Reliability Evaluation",
        "condition": "A",
        "condition_name": "Direct LLM",
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

    # Extract files mentioned by the generated patch
    for line in patch.splitlines():
        if line.startswith("+++ b/"):
            result["localized_files"].append(
                line[6:]
            )

    # Condition A does not perform automated
    # repository validation.
    result["issue_resolved"] = False
    result["patch_accepted"] = False
    result["tests_passed"] = False

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    result_path = (
        RESULTS_DIR
        / f"condition_A_issue_{issue_id}.json"
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

    result = run_condition_a(
        issue_id=3,
        repository_path=(
            r"C:\Users\Rahul\RepoFix-AI"
        ),
    )

    print(json.dumps(result, indent=2))