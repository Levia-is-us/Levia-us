import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework.tool_runner import ToolRunner
from engine.tool_framework import simple_tool

from tools.website_scan_tool.utils import (
    get_all_content,
    get_all_links,
    remove_duplicate_links,
    get_prompt_links,
    get_summary_links,
)



@simple_tool("Website Scan Tool")
def website_scan(urls: list, intent: str):
    try:
        raw_links = get_all_links(urls)
        unique_links = remove_duplicate_links(raw_links)
        filtered_links = get_prompt_links(unique_links, intent)
        links_with_content = get_all_content(filtered_links)
        summary = get_summary_links(links_with_content, intent)
        return summary
    except Exception as e:
        return


def main():
    tool = website_scan()
    runner = ToolRunner(tool)
    runner.run()


if __name__ == "__main__":
    main()
