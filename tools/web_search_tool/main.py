import sys
import os


project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from tools.web_search_tool.util import (
    extract_relevance_url,
    generate_search_keywords,
    search_non_visual,
    search_visual,
)


from engine.tool_framework import run_tool, BaseTool


@run_tool
class WebSearchTool(BaseTool):
    """
    This tool is used to search the web for information.
    Args:
        intent (str): The intent of the user.
    Returns:
        A list of URLs.
    """

    def web_search(self, intent: str):
        # Generate search keywords
        keywords = generate_search_keywords(intent)

        # Perform web search
        content_list = search_visual(keywords)

        if not content_list:
            return "No results found."
        else:
            # Extract relevance URLs
            contents = " ".join(content_list)
            relevance_urls = extract_relevance_url(intent, contents)
            if not relevance_urls:
                return "No results found."
            return relevance_urls
