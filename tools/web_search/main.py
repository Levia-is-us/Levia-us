import sys
import os

from aipolabs import Aipolabs
from aipolabs.types.functions import FunctionExecutionResult

from tools.web_search.util import (
    aipolabs_search,
    extract_relevance_url,
    generate_search_keywords,
)

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework.tool_runner import ToolRunner
from engine.tool_framework import simple_tool


@simple_tool("Web Search Tool")
def web_search(intent: str):
    """
    This tool is used to search the web for information.
    Args:
        intent (str): The intent of the user.
    Returns:
        A list of URLs that match the intent.
    """

    # Generate search keywords
    keywords = generate_search_keywords(intent)

    # Initialize search engine
    client = Aipolabs(api_key=os.environ.get("AIPOLABS_API_KEY"))

    content_list = []
    for keyword in keywords:
        try:
            # Search for each keyword
            result: FunctionExecutionResult = aipolabs_search(client, keyword)
            # Extract content from search results
            contents = [
                f'url: {result["url"]} content: {result["content"]}'
                for result in result.data["results"]
            ]
            content_list.extend(contents)
        except Exception as e:
            print(f"Aipolabs search error: {str(e)}")

    if not content_list:
        return "No results found."
    else:
        # Extract relevance URLs
        relevance_urls = extract_relevance_url(intent, content_list)
        if not relevance_urls:
            return "No results found."
        return relevance_urls


def main():
    tool = web_search()
    runner = ToolRunner(tool)
    runner.run()


if __name__ == "__main__":
    main()
