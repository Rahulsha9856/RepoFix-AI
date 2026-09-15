from repofix.agents.issue_analyzer import IssueAnalyzer
from repofix.agents.llm_client import LLMClient
from repofix.analyzers.static_analyzer import StaticAnalyzer
from repofix.retrieval.retriever import RepositoryRetriever


class RepositoryAgent:
    def __init__(self) -> None:
        self.issue_analyzer = IssueAnalyzer()
        self.retriever = RepositoryRetriever()
        self.analyzer = StaticAnalyzer()
        self.llm = LLMClient()

    def analyze_issue(
        self,
        repository_path: str,
        title: str,
        description: str | None,
    ) -> dict:
        analysis = self.issue_analyzer.analyze(
            title,
            description,
        )

        query = " ".join(analysis.keywords)

        relevant_files = self.retriever.search(
            repository_path,
            query,
        )[:10]

        context_parts = []

        for file in relevant_files:
            context_parts.append(
                f"FILE: {file['path']}\n"
                f"{file['content']}"
            )

        repository_context = "\n\n".join(context_parts)

        static_results = self.analyzer.analyze(
            repository_path,
        )

        prompt = f"""
You are RepoFix AI, a repository-aware software debugging agent.

GitHub Issue:
Title: {analysis.title}

Description:
{analysis.description}

Relevant repository files:
{repository_context}

Static analysis results:

Ruff:
{static_results["ruff"]}

Bandit:
{static_results["bandit"]}

Analyze the issue and explain:

1. What is likely causing the problem?
2. Which file is most likely responsible?
3. What code change should be made?
4. Do the static-analysis results reveal anything relevant?

Do not modify files yet.
"""

        reasoning = self.llm.generate(prompt)

        return {
            "issue": {
                "title": analysis.title,
                "description": analysis.description,
                "keywords": analysis.keywords,
            },
            "relevant_files": relevant_files,
            "static_analysis": static_results,
            "reasoning": reasoning,
        }