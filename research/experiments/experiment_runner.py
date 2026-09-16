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


from repofix.agents.fix_agent import FixAgent


# Experiment configuration
CONFIG_PATH = (
    Path(__file__).resolve().parent
    / "experiment_config.json"
)


# Experiment results directory
RESULTS_DIR = (
    Path(__file__).resolve().parents[1]
    / "results"
)


def load_experiment_config() -> dict:
    """Load the experiment configuration."""
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_condition(condition_id: str) -> dict:
    """Return configuration for a specific experiment condition."""
    config = load_experiment_config()
    return config["conditions"][condition_id]


def create_result(condition_id: str, issue_id: int) -> dict:
    """Create an empty experiment result."""
    condition = get_condition(condition_id)

    return {
        "experiment": "RepoFix AI Reliability Evaluation",
        "condition": condition_id,
        "condition_name": condition["name"],
        "issue_id": issue_id,
        "success": False,
        "issue_resolved": False,
        "patch_accepted": False,
        "tests_passed": False,
        "incorrect_modification": False,
        "retry_count": 0,
        "localized_files": [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def update_result_from_fix(
    result: dict,
    fix_result: dict,
) -> dict:
    """Convert FixAgent output into experiment metrics."""

    attempts = fix_result.get("attempts", [])

    result["success"] = bool(
        fix_result.get("success", False)
    )

    result["issue_resolved"] = result["success"]

    result["patch_accepted"] = any(
        attempt.get("status") == "validated"
        for attempt in attempts
    )

    result["tests_passed"] = any(
        attempt.get("status") == "validated"
        for attempt in attempts
    )

    result["retry_count"] = max(
        0,
        len(attempts) - 1,
    )

    # Extract files modified by the final patch
    final_patch = fix_result.get("final_patch") or ""

    localized_files = []

    for line in final_patch.splitlines():
        if line.startswith("+++ b/"):
            localized_files.append(line[6:])

    result["localized_files"] = localized_files

    return result


def save_result(result: dict) -> Path:
    """Save an experiment result as JSON."""

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    condition_id = result["condition"]

    issue_id = result["issue_id"]

    result_path = (
        RESULTS_DIR
        / f"condition_{condition_id}_issue_{issue_id}.json"
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

    return result_path


def run_condition_c(
    issue_id: int,
    repository_path: str,
) -> dict:
    """Run the complete RepoFix AI experiment condition."""

    result = create_result(
        condition_id="C",
        issue_id=issue_id,
    )

    agent = FixAgent()

    fix_result = agent.run(
        repository_path=repository_path,
        issue_title="Fix calculator addition bug",
        issue_description=(
            "The add function in demo_bug/calculator.py "
            "is incorrect. It should return the sum of a and b."
        ),
        relevant_files=[],
        static_analysis={
            "ruff": "No issues",
            "bandit": "No issues",
        },
        reasoning="Fix the calculator addition bug.",
    )

    result = update_result_from_fix(
        result,
        fix_result,
    )

    save_result(result)

    return result


if __name__ == "__main__":

    config = load_experiment_config()

    print(
        config["experiment"]
    )

    for condition_id in config["conditions"]:

        result = create_result(
            condition_id=condition_id,
            issue_id=3,
        )

        print(result)