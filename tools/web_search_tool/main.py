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


@run_tool()
class WebSearchTool(BaseTool):
    """Tool for searching web content"""
    
    def web_search(self, intent: str):
        """
        This tool is used to search the web for information.
        Args:
            intent (str): The intent of the user.
        Returns:
            A list of URLs that match the intent.
        """
        # Generate search keywords
        keywords = generate_search_keywords(intent)

        # Perform web search
        is_visual = os.getenv("VISUAL")
        if is_visual == "T":
            content_list = search_visual(keywords)
        else:
            content_list = search_non_visual(keywords)

        if not content_list:
            return "No results found."
        else:
            # Extract relevance URLs
            relevance_urls = extract_relevance_url(intent, content_list)
            if not relevance_urls:
                return "No results found."
            return relevance_urls


