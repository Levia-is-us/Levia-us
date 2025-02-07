

import os
import sys

from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)
sys.path.append(project_root)

from engine.tool_framework.tool_run import run_tool
from engine.tool_framework import ToolRegistry, ToolCaller
from fileManage import get_top_title_with_hash


def main():
    # print(project_root)
    # Create and initialize ToolRegistry
    registry = ToolRegistry()
    
    # Use absolute path
    tools_dir = os.path.join(os.path.dirname(__file__), "./")
    registry.scan_directory(tools_dir)  # Scan tools directory

    # Create ToolCaller instance
    caller = ToolCaller(registry)

    # List all available tools
    tools = registry.list_tools()
    print("Available tools:", len(tools))
    for tool in tools:
        print(f"Tool: {tool['name']}")
        print(f"Description: {tool['description']}")
        print("Methods:")
        for method, info in tool['methods'].items():
            print(f" - {method}{info['signature']}")

    # Call tool and handle result
    print("\nCalling location tool...")


    markdown_text = """
      # TITLE

      This is a **bold1111** text.

      - List item 1
      - List item 2
      """
    

    article_title = get_top_title_with_hash(markdown_text)
    print("Please input markdown or string content!",article_title, file=sys.stderr)
    
    # The article title must be a Markdown first-level heading
    params={
        "content":markdown_text,
        "gitbook_api_key":'',
        "azure_file_server_key":'',
        "user_website_url":""
    }

    result = caller.call_tool(
        "save_markdown_to_gitbook_tool", 
        "save_markdown_to_gitbook", 
        params
    )
    
    if result:
        if 'error' in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"Location info: {result}")
    else:
        print("Tool call failed, no result returned")

if __name__ == "__main__":
    main()


