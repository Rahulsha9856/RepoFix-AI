import json
import sys
from datetime import datetime, timezone
from pathlib import Path


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
    issue_title: str,
    issue_description: str,
) -> dict:
    """
    Condition A:
    GitHub Issue -> Direct LLM -> Patch
    """

    llm = LLMClient()

    prompt = f"""
You are fixing a GitHub issue.

Issue title:
{issue_title}

Issue description:
{issue_description}

Generate ONLY a unified Git diff containing
the required fix.

Do not analyze the repository.
Do not retrieve additional files.
Do not run tests.
Return only the patch.
"""

    patch = llm.generate(prompt)

    localized_files = []

    for line in patch.splitlines():
        if line.startswith("+++ b/"):
            localized_files.append(line[6:])

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
        "localized_files": localized_files,
        "patch": patch,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }

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
        issue_id=4,
        issue_title="Fix multiplication bug",
        issue_description=(
            "The multiply function in "
            "demo_bug/multiply.py is incorrect. "
            "It currently adds a and b, but it should "
            "return the product of a and b. "
            "Expected behavior: multiply(4, 5) should "
            "return 20."
        ),
    )

    print(
        json.dumps(
            result,
            indent=2,
        )
    )