import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from tools.smithery_mcp_tool.main import SmitheryMCPTool

def main():
    mcp_tool = SmitheryMCPTool()

    arguments = {"lat": 37.7749, "lng": -122.4194, "adjacents": True, "responseType": "long"}
    result = mcp_tool.mcp_call_tool(serverId="@blake365/macrostrat-mcp", toolName="find-columns", arguments=arguments)
    print(result)

if __name__ == "__main__":
    main()

