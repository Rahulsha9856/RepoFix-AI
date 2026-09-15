import json
from datetime import datetime, timezone
from pathlib import Path


CONFIG_PATH = (
    Path(__file__).resolve().parent
    / "experiment_config.json"
)


def load_experiment_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_condition(condition_id: str) -> dict:
    config = load_experiment_config()
    return config["conditions"][condition_id]


def create_result(
    condition_id: str,
    issue_id: int,
) -> dict:
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
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }

def update_result_from_fix(
    result: dict,
    fix_result: dict,
) -> dict:
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

    return result


if __name__ == "__main__":
    config = load_experiment_config()

    print(config["experiment"])

    for condition_id in config["conditions"]:
        result = create_result(
            condition_id=condition_id,
            issue_id=3,
        )

        print(result)