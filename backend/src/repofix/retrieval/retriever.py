from repofix.retrieval.indexer import RepositoryIndexer


class RepositoryRetriever:
    def __init__(self) -> None:
        self.indexer = RepositoryIndexer()

    def search(
        self,
        repository_path: str,
        query: str,
    ) -> list[dict[str, str]]:
        index = self.indexer.build_index(
            repository_path
        )

        keywords = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        results: list[dict[str, str]] = []

        for item in index:
            path = item["path"].lower()
            content = item["content"].lower()

            score = 0

            # Strongly prioritize filename/path matches
            for keyword in keywords:
                if keyword in path:
                    score += 5

                if keyword in content:
                    score += 1

            if score > 0:
                results.append(
                    {
                        "path": item["path"],
                        "content": item["content"],
                        "score": str(score),
                    }
                )

        results.sort(
            key=lambda item: int(item["score"]),
            reverse=True,
        )

        return results