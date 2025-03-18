import base64
import json
import os
import sys
from dotenv import load_dotenv
import inspect
import requests

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)
sys.path.append(project_root)

from engine.tool_framework import run_tool, BaseTool


MCP_REPO_URL=os.getenv("MCP_REPO_URL", "")

@run_tool()
class SmitheryMCPTool(BaseTool):
    """Tool for listing available abilities"""
    
    def mcp_call_tool(self, serverId: str, toolName: str, arguments: dict, config: dict = None) -> dict: 
        """List all available abilities"""
        # /api/mcpCallTool?serverId=@truss44/mcp-crypto-price&toolName=get-crypto-price
        arguments = {
                "arguments": arguments
        }
        url = f"{MCP_REPO_URL}/api/mcpCallTool?serverId={serverId}&toolName={toolName}&userId=levia"
        if config:
            config_base64 = base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')
            url = f"{MCP_REPO_URL}/api/mcpCallTool?serverId={serverId}&toolName={toolName}&userId=levia&config={config_base64}"
        
        response = requests.post(url, json=arguments)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": "Failed to fetch MCP response; Details: " + response.text}
        
    
