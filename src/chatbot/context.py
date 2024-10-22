from langchain_community.utilities import SerpAPIWrapper

from settings import SERPAPI_API_KEY


class SearchContext:
    def __init__(self):
        self.searcher = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

    def generate_context(self, question: str) -> list[str]:
        result = self.searcher.run(question)
        if isinstance(result, list):
            return [str(item) for item in result]
        return result.split("', '")
