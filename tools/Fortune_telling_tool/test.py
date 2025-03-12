import os
import sys

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller


def main():
    registry = ToolRegistry()
    tools_dir = os.path.join(project_root, "tools")
    registry.scan_directory(tools_dir)

    caller = ToolCaller(registry)

    # List all available tools
    tools = registry.list_tools()
    print("Available tools:", len(tools))
    for tool in tools:
        print(f"Tool: {tool['name']}")
        print(f"Description: {tool['description']}")
        print("Methods:")
        for method, info in tool["methods"].items():
            print(f" - {method}{info['signature']}")

    concern = [{"role": "user", "content": "I born in 12/21/1994, I was born on December 21, 1994. Please tell me my fortune this year. please give me some advice"}]

    result = caller.call_tool(
        tool_name="FortuneTellingTool",
        method="fortune_telling",
        kwargs={"user_concern": concern},
    )

    if result:
        if "error" in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"response info: {result}")
    else:
        print("Tool call failed, no result returned")


if __name__ == "__main__":
    main()
