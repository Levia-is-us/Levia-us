import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from tools.smithery_mcp_tool.main import SmitheryMCPTool

def main():
    mcp_tool = SmitheryMCPTool()

    arguments = {
        "arguments": {
            "symbol": "ETH"
        }
    }
    result = mcp_tool.mcp_call_tool(serverId="@truss44/mcp-crypto-price", toolName="get-crypto-price", arguments=arguments)
    print(result)

if __name__ == "__main__":
    main()

