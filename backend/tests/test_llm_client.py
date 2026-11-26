
import pytest

from repofix.agents.llm_client import LLMClient
from repofix.core.config import settings


@pytest.fixture
def mock_llm(monkeypatch):
    monkeypatch.setattr(settings, "use_mock_llm", True)
    return LLMClient()


def test_multiplication_patch(mock_llm):
    prompt = "Fix multiplication bug in demo_bug/multiply.py"

    patch = mock_llm.generate(prompt)

    assert "demo_bug/multiply.py" in patch
    assert "-    return a + b" in patch
    assert "+    return a * b" in patch


def test_addition_patch(mock_llm):
    prompt = (
        "Fix calculator addition bug. "
        "The function should return the sum."
    )

    patch = mock_llm.generate(prompt)

    assert "demo_bug/calculator.py" in patch
    assert "-    return a - b" in patch
    assert "+    return a + b" in patch


def test_multiplication_takes_priority(mock_llm):
    prompt = (
        "Fix multiplication bug in demo_bug/calculator.py. "
        "The multiply(a, b) function is incorrect."
    )

    patch = mock_llm.generate(prompt)

    assert "demo_bug/multiply.py" in patch
    assert "+    return a * b" in patch
    assert "demo_bug/calculator.py" not in patch


def test_unsupported_prompt(mock_llm):
    prompt = "Fix an unrelated authentication bug."

    result = mock_llm.generate(prompt)

    assert "No mock patch is available" in result
    assert "diff --git" not in result
