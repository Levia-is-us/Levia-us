from typing import Optional, Dict, List, Any
from .tool_registry import ToolRegistry
import subprocess
import json
import sys
import os


class ToolCaller:
    """Class for calling tools"""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def call_tool(self, tool_name: str, method: str, kwargs: dict = None):
        """Call a tool method"""
        try:
            # Get tool instance
            tool_info = self.registry.get_tool(tool_name)
            if not tool_info:
                return {"error": f"Tool '{tool_name}' not found", "status": "failure"}

            # Get instance from tool info
            tool_instance = tool_info["instance"]
            
            # Get method
            tool_method = getattr(tool_instance, method, None)
            if not tool_method:
                return {"error": f"Method '{method}' not found in tool '{tool_name}'", "status": "failure"}

            # Execute method
            result = tool_method(**kwargs) if kwargs else tool_method()
            
            # Return result if not None
            if result is not None:
                return result
            else:
                return {"error": "Tool execution returned None", "status": "failure"}

        except Exception as e:
            print(f"Tool execution error: {str(e)}", file=sys.stderr)
            return {"error": str(e), "status": "failure"}

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return self.registry.list_tools()