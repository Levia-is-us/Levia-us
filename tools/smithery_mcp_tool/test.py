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
        'to': 'armorn@outlook.com', 'subject': 'test email', 'content': 'hello!'
        }
    result = mcp_tool.mcp_call_tool(serverId="@ykhli/mcp-send-emails", toolName="send-email", arguments=arguments)
    print(result)

if __name__ == "__main__":
    main()

