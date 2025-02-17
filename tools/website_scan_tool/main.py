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
        try:
            raw_links = get_all_links(url_list)
            unique_links = remove_duplicate_links(raw_links)
            filtered_links = get_prompt_links(unique_links, intent)
            links_with_content = get_all_content(filtered_links)
            summary = get_summary_links(links_with_content, intent)
            return summary
        except Exception as e:
            if(str(e) == "website connection timeout"):
                return "website connection timeout"
            else:
                raise Exception(e)