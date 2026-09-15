from repofix.agents.llm_client import LLMClient


class PatchGenerator:
    def __init__(self) -> None:
        self.llm = LLMClient()

    def generate_patch(
        self,
        issue_title: str,
        issue_description: str,
        relevant_files: list[dict[str, str]],
        static_analysis: dict[str, str],
        reasoning: str,
    ) -> str:
        files_context = "\n\n".join(
            f"FILE: {file['path']}\n{file['content']}"
            for file in relevant_files
        )

        prompt = f"""
You are RepoFix AI, an autonomous software repair agent.

GitHub Issue:
Title: {issue_title}

Description:
{issue_description}

Previous analysis:
{reasoning}

Relevant repository files:
{files_context}

Static analysis:

Ruff:
{static_analysis["ruff"]}

Bandit:
{static_analysis["bandit"]}

Generate a unified Git diff that fixes the issue.

Rules:
1. Modify only files necessary to fix the issue.
2. Preserve existing functionality.
3. Do not include explanations.
4. Return ONLY the unified diff.
5. The diff must be directly applicable with git apply.
"""

        return self.llm.generate(prompt)