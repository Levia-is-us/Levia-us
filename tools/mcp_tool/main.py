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


MCP_REPO_URL=os.getenv("LEVIA_MCP_REPO_URL", "")

@run_tool()
class MCPTool(BaseTool):
    """Tool for listing available abilities"""
    
    def mcp_call_tool(self, serverId: str, toolName: str, arguments: dict) -> dict: 
        """List all available abilities"""
        # /api/mcpCallTool?serverId=@truss44/mcp-crypto-price&toolName=get-crypto-price
        url = f"{MCP_REPO_URL}/api/mcpCallTool?serverId={serverId}&toolName={toolName}"
        
        response = requests.post(url, json=arguments)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": "Failed to fetch MCP list"}
        
    
