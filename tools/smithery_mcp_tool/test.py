# import sys
# import os
# 
# project_root = os.path.dirname(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# )
# sys.path.append(project_root)
# 
# from tools.smithery_mcp_tool.main import SmitheryMCPTool
# 
# def main():
#     mcp_tool = SmitheryMCPTool()
# 
#     arguments = {"lat": 37.7749, "lng": -122.4194, "adjacents": True, "responseType": "long"}
#     result = mcp_tool.mcp_call_tool(serverId="@blake365/macrostrat-mcp", toolName="find-columns", arguments=arguments)
#     print(result)
# 
# if __name__ == "__main__":
#     main()

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
    arguments = {"lat": 37.7749, "lng": -122.4194, "adjacents": True, "responseType": "long"}

    result = caller.call_tool(
        tool_name="SmitheryMCPTool",
        method="mcp_call_tool",
        kwargs={
            "serverId": "@blake365/macrostrat-mcp",
            "toolName": "find-columns",
            "arguments": arguments
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