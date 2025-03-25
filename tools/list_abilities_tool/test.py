import os
import sys
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
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
    tool_list = []
    for tool in tools:
        tool_list.append({
            "name": tool['name'],
            "description": tool['description']
        })
    print(f"tool_list: {tool_list}")
    
    result = caller.call_tool(tool_name="ListAbilitiesTool", method="list_abilities", kwargs={})
    
    if result:
        if 'error' in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"response info: {result}")
    else:
        print("Tool call failed, no result returned")

if __name__ == "__main__":
    main()

