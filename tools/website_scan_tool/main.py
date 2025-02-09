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
    links = get_all_links(urls)
    links = remove_duplicate_links(links)
    links = get_prompt_links(links, intent)
    links = get_all_content(links)
    result = get_summary_links(links, intent)
    return result


def main():
    tool = website_scan()
    runner = ToolRunner(tool)
    runner.run()


if __name__ == "__main__":
    main()
