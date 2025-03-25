import json
import os
import sys
from dotenv import load_dotenv
import inspect


project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)
sys.path.append(project_root)

from engine.tool_framework import run_tool, BaseTool


@run_tool("List Abilities Tool")
class ListAbilitiesTool(BaseTool):
    """Tool for listing available abilities"""
    
    def list_abilities(self) -> dict: 
        """List all available abilities"""
        abilities = {}
        for method_name, method in self.methods.items():
            try:
                if hasattr(method, '__code__'):
                    arg_count = method.__code__.co_argcount
                    args = method.__code__.co_varnames[:arg_count]
                    signature = f"({', '.join(args)})"
                else:
                    signature = "(...)"
                    
                abilities[method_name] = {
                    "description": self.get_method_description(method_name),
                    "signature": signature
                }
            except Exception:
                abilities[method_name] = {
                    "description": self.get_method_description(method_name),
                    "signature": "(...)"
                }
        return abilities
    
