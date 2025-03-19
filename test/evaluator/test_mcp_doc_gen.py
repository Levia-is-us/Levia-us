import base64
import json
import sys
import os
import requests


# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))


# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from engine.flow.mcp_adaption_flow.mcp_adaption_flow import (
    mcp_adaption_flow,
)


def get_mcp_tools(server_id):
    response = requests.get(
        f"https://levia-mcp-repo.azurewebsites.net/api/mcpTools?serverId={server_id}&userId=levia"
    )
    return response.json()


# def call_mcp_tool(server_id, tool_name, arguments, config):
#     body = {
#         "arguments": arguments,
#     }
#     base64_config = base64.b64encode(json.dumps(config).encode("utf-8")).decode("utf-8")
#     response = requests.post(
#         f"https://levia-mcp-repo.azurewebsites.net/api/mcpCallTool?serverId={server_id}&toolName={tool_name}",
#         json=body,
#     )
#     return response.json()


def process_mcp_tool(server_id):
    mcp_info = get_mcp_tools(server_id)
    for tool in mcp_info["tools"]:
        print(tool)
        doc = mcp_adaption_flow(tool, server_id)
        print(doc)


if __name__ == "__main__":
    process_mcp_tool("@ykhli/mcp-send-emails")
