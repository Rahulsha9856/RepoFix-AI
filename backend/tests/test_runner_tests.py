
from pathlib import Path

from repofix.testing.test_runner import TestRunner


def test_multiplication_patch_runs_multiplication_test(tmp_path):
    demo_bug = tmp_path / "demo_bug"
    demo_bug.mkdir()

    (demo_bug / "multiply.py").write_text(
        "def multiply(a, b):\n"
        "    return a * b\n",
        encoding="utf-8",
    )

    (demo_bug / "test_multiply.py").write_text(
        "from multiply import multiply\n\n"
        "def test_multiply():\n"
        "    assert multiply(4, 5) == 20\n",
        encoding="utf-8",
    )

    (demo_bug / "test_calculator.py").write_text(
        "def test_unrelated():\n"
        "    assert False\n",
        encoding="utf-8",
    )

    patch = (
        "diff --git a/demo_bug/multiply.py b/demo_bug/multiply.py\n"
        "--- a/demo_bug/multiply.py\n"
        "+++ b/demo_bug/multiply.py\n"
    )

    result = TestRunner().run_pytest(str(tmp_path), patch)

    assert result["success"] is True
    assert result["test_files"] == [
        "demo_bug/test_multiply.py"
    ]


def test_calculator_patch_runs_calculator_test(tmp_path):
    demo_bug = tmp_path / "demo_bug"
    demo_bug.mkdir()

    (demo_bug / "calculator.py").write_text(
        "def add(a, b):\n"
        "    return a + b\n",
        encoding="utf-8",
    )

    (demo_bug / "test_calculator.py").write_text(
        "from calculator import add\n\n"
        "def test_add():\n"
        "    assert add(2, 3) == 5\n",
        encoding="utf-8",
    )

    patch = (
        "diff --git a/demo_bug/calculator.py b/demo_bug/calculator.py\n"
        "--- a/demo_bug/calculator.py\n"
        "+++ b/demo_bug/calculator.py\n"
    )

    result = TestRunner().run_pytest(str(tmp_path), patch)

    assert result["success"] is True
    assert result["test_files"] == [
        "demo_bug/test_calculator.py"
    ]
