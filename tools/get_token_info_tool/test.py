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
    
    
    result = caller.call_tool(tool_name="GetTokenInfoTool", method="get_token_info", kwargs={"token_address": "4voSriVommQjWGpULifpwiywFZXdwuaTJ61qRU2mpump"})
    
    if result:
        if "error" in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"response info: {result}")
    else:
        print("Tool call failed, no result returned")


if __name__ == "__main__":
    main()