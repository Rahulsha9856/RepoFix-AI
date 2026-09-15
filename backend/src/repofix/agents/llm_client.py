from google import genai

from repofix.core.config import settings


class LLMClient:
    def __init__(self) -> None:
        self.client = None

        if not settings.use_mock_llm:
            if not settings.gemini_api_key:
                raise ValueError(
                    "GEMINI_API_KEY is not configured"
                )

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    def generate(self, prompt: str) -> str:
        if settings.use_mock_llm:
            if "Generate a unified Git diff" in prompt:
                return (
                    "diff --git a/demo_bug/calculator.py "
                    "b/demo_bug/calculator.py\n"
                    "--- a/demo_bug/calculator.py\n"
                    "+++ b/demo_bug/calculator.py\n"
                    "@@ -1,2 +1,2 @@\n"
                    " def add(a, b):\n"
                    "-    return a - b\n"
                    "+    return a + b\n"
                )

            return (
                "Mock RepoFix analysis: "
                "repository context was retrieved successfully. "
                "The issue should be investigated using the "
                "retrieved files and automated tests."
            )

        interaction = self.client.interactions.create(
            model=settings.gemini_model,
            input=prompt,
        )

        return interaction.output_text