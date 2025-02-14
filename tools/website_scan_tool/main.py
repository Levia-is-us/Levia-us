import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework import run_tool, BaseTool

from tools.website_scan_tool.utils import (
    get_all_content,
    get_all_links,
    remove_duplicate_links,
    get_prompt_links,
    get_summary_links,
)



@run_tool("Website Scan Tool")
class WebsiteScanTool(BaseTool):
    """Tool for scanning website content"""
    
    def website_scan(self, url_list: list, intent: str):
        """
        Scan websites and extract relevant information
        Args:
            url_list: List of URLs to scan
            intent: The intent to guide the scanning
        Returns:
            Extracted information
        """
        links = get_all_links(url_list)
        links = remove_duplicate_links(links)
        links = get_prompt_links(links, intent)
        links = get_all_content(links)
        result = get_summary_links(links, intent)
        return result