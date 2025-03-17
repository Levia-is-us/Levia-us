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
from memory.episodic_memory.episodic_memory import store_short_pass_memory


def get_mcp_tools(server_id, user_id="levia"):
    response = requests.get(
        f"https://levia-mcp-repo.azurewebsites.net/api/mcpTools?serverId={server_id}&userId={user_id}"
    )
    return response.json()


def call_mcp_tool(server_id, tool_name, arguments):
    body = {
        "arguments": arguments,
    }
    response = requests.post(
        f"https://levia-mcp-repo.azurewebsites.net/api/mcpCallTool?serverId={server_id}&toolName={tool_name}",
        json=body,
    )
    return response.json()


def process_mcp_tool(server_id):
    mcp_info = get_mcp_tools(server_id)
    for tool in mcp_info["tools"]:
        json_data = mcp_adaption_flow(tool, server_id)
        server_id = json_data["server_id"]
        tool_name = json_data["tool_name"]
        source = json_data["source"]
        for function in json_data["functions"]:
            detailed_description = function.pop("detailed_description")
            short_description = function.pop("short_description")
            metadata = {
                "method": "mcp_call_tool", #function["method"],
                "tool": "SmitheryMCPTool",
                "data": json.dumps(function),
                "short_description": short_description,
                "description": detailed_description,
                "details": detailed_description,
                "source": source,
            }

            store_short_pass_memory(
                "smithery_mcp_tool" + "-" + server_id + "-" + tool_name,
                short_description,
                metadata,
            )


if __name__ == "__main__":
    process_mcp_tool("@ykhli/mcp-send-emails")
