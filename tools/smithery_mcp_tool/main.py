import os
import sys
from dotenv import load_dotenv
import smithery
import mcp
import asyncio
from mcp.client.websocket import websocket_client

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
        async def _async_call():
            try:
                url = smithery.create_smithery_url(f"wss://server.smithery.ai/{serverId}/ws", {})
                # Connect to the server using websocket client
                async with websocket_client(url) as streams:
                    async with mcp.ClientSession(*streams) as session:
                        # Example: Call a tool
                        result = await session.call_tool(toolName, arguments)
                return result
            except Exception as e:
                return {"error": str(e)}

        try:
            return asyncio.run(_async_call())
        except Exception as e:
            return {"error": str(e)}


    
