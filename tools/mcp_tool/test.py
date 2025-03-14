import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from tools.mcp_tool.main import MCPTool

def main():
    mcp_tool = MCPTool()

    arguments = {
        "arguments": {
            "symbol": "BTC"
        }
    }
    result = mcp_tool.mcp_call_tool(serverId="@truss44/mcp-crypto-price", toolName="get-crypto-price", arguments=arguments)
    print(result)

if __name__ == "__main__":
    main()

