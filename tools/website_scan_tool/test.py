import os
import sys
import dotenv

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller


def main():
    registry = ToolRegistry()
    tools_dir = os.path.join(project_root, "tools")
    registry.scan_directory(tools_dir)

    caller = ToolCaller(registry)
    result = caller.call_tool(
        tool_name="WebsiteScanTool",
        method="website_scan",
        kwargs={
            "url_list": ["https://leviaprotocol.gitbook.io/leviaprotocol"],
            "intent": "What is Levia,and how it works?"
        }
    )

    if result:
        if "error" in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"Success: {result}")
    else:
        print("Tool call failed, no result returned")


if __name__ == "__main__":
    main()
