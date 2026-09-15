from dataclasses import dataclass


@dataclass
class IssueAnalysis:
    title: str
    description: str
    keywords: list[str]


class IssueAnalyzer:
    def analyze(
        self,
        title: str,
        description: str | None,
    ) -> IssueAnalysis:
        description = description or ""

        text = f"{title} {description}".lower()

        words = {
            word.strip(".,!?():;")
            for word in text.split()
            if len(word.strip(".,!?():;")) > 2
        }

        keywords = sorted(words)

        return IssueAnalysis(
            title=title,
            description=description,
            keywords=keywords,
        )