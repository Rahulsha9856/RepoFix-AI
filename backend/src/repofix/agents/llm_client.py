from google import genai

from repofix.core.config import settings


class LLMClient:
    def __init__(self):
        self.client = None

        if not settings.use_mock_llm:
            if not settings.gemini_api_key:
                raise ValueError("GEMINI_API_KEY is not configured")

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    def generate(self, prompt: str) -> str:
        if settings.use_mock_llm:
            prompt_lower = prompt.lower()

            # Handle the calculator addition issue first.
            if (
                "fix calculator addition bug" in prompt_lower
                or (
                    "demo_bug/calculator.py" in prompt_lower
                    and "should return the sum" in prompt_lower
                )
            ):
                return """diff --git a/demo_bug/calculator.py b/demo_bug/calculator.py
--- a/demo_bug/calculator.py
+++ b/demo_bug/calculator.py
@@ -1,2 +1,2 @@
 def add(a, b):
-    return a - b
+    return a + b
"""

            # Handle the multiplication issue.
            if (
                "fix multiplication bug" in prompt_lower
                or "multiplication bug" in prompt_lower
            ):
                return """diff --git a/demo_bug/multiply.py b/demo_bug/multiply.py
--- a/demo_bug/multiply.py
+++ b/demo_bug/multiply.py
@@ -1,2 +1,2 @@
 def multiply(a, b):
-    return a + b
+    return a * b
"""

            # Generic mock response for other prompts.
            return (
                "Analyze the issue and identify the relevant code. "
                "No mock patch is available for this specific issue."
            )

        if self.client is None:
            raise RuntimeError("LLM client is not initialized")

        interaction = self.client.interactions.create(
            model=settings.gemini_model,
            input=prompt,
        )

        return interaction.output_text