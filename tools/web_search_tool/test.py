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
    
    # Use absolute path
    tools_dir = os.path.join(project_root, "tools")
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
    
    result = caller.call_tool(tool_name="WebSearchTool", method="web_search", kwargs={'intent': "User requests Apple's iPhone sales growth data for Q4 2023 and current AAPL stock price"})
    
    if result:
        if "error" in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"response info: {result}")
    else:
        print("Tool call failed, no result returned")


if __name__ == "__main__":
    main()