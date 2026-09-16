import json
from pathlib import Path


RESULTS_DIR = (
    Path(__file__).resolve().parents[1]
    / "results"
)


CONDITIONS = ["A", "B", "C"]


def load_result(condition: str, issue_id: int = 3) -> dict:
    """Load one experiment result."""

    path = (
        RESULTS_DIR
        / f"condition_{condition}_issue_{issue_id}.json"
    )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def calculate_metrics(issue_id: int = 3) -> dict:
    """Calculate comparison metrics for all conditions."""

    results = {
        condition: load_result(
            condition,
            issue_id,
        )
        for condition in CONDITIONS
    }

    metrics = {}

    for condition, result in results.items():
        metrics[condition] = {
            "condition_name": result["condition_name"],
            "issue_resolution_rate": (
                1 if result["issue_resolved"] else 0
            ),
            "patch_acceptance_rate": (
                1 if result["patch_accepted"] else 0
            ),
            "test_pass_rate": (
                1 if result["tests_passed"] else 0
            ),
            "incorrect_modification_rate": (
                1 if result["incorrect_modification"] else 0
            ),
            "average_retries": result["retry_count"],
            "localized_files": result["localized_files"],
        }

    return {
        "experiment": "RepoFix AI Reliability Evaluation",
        "issue_id": issue_id,
        "conditions": metrics,
    }


def save_metrics(
    metrics: dict,
    issue_id: int = 3,
) -> Path:
    """Save the calculated metrics."""

    output_path = (
        RESULTS_DIR
        / f"metrics_issue_{issue_id}.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics,
            file,
            indent=2,
        )

    return output_path


if __name__ == "__main__":

    metrics = calculate_metrics()

    save_metrics(metrics)

    print(
        json.dumps(
            metrics,
            indent=2,
        )
    )