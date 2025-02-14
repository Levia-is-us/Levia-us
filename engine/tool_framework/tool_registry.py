import sys
import inspect
import importlib.util
import os
from typing import Dict, Any, Optional, Type, List
from .base_tool import BaseTool



from pathlib import Path


class ToolRegistry:
    """Registry for all tools"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
            cls._instance.tool_paths = {}
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_tools"):
            self._tools: Dict[str, dict] = {}
            self.tool_paths: Dict[str, str] = {}

    def register_tool(self, tool_class: Type[BaseTool], file_path: str) -> None:
        """Register a tool class"""
        try:
            # Use class name as tool name
            tool_name = tool_class.__name__
            print(f"Registering tool: {tool_name} from {file_path}")
            
            # Create tool instance and store in dictionary
            self._tools[tool_name] = {
                "class": tool_class,
                "instance": tool_class(),
                "file": file_path
            }
            
        except Exception as e:
            print(f"Failed to register tool {tool_class.__name__}: {e}", file=sys.stderr)

    def get_tool(self, tool_name: str) -> Optional[dict]:
        """Get a tool by name"""
        return self._tools.get(tool_name)

    def get_tool_path(self, tool_name: str) -> Optional[str]:
        """Get tool script path by name"""
        return self.tool_paths.get(tool_name)

    def list_tools(self) -> list:
        """List all registered tools"""
        tools_info = []
        for name, tool in self._tools.items():
            tool_info = {
                "name": name,
                "description": tool["instance"]._description,
                "methods": {}
            }
            
            # Use safer way to get method information
            for method_name, method in tool["instance"].methods.items():
                try:
                    # Try to get method parameters
                    if hasattr(method, '__code__'):
                        arg_count = method.__code__.co_argcount
                        args = method.__code__.co_varnames[:arg_count]
                        signature = f"({', '.join(args)})"
                    else:
                        signature = "(...)"
                        
                    tool_info["methods"][method_name] = {
                        "description": tool["instance"].get_method_description(method_name),
                        "signature": signature
                    }
                except Exception:
                    # Use default signature if any error occurs
                    tool_info["methods"][method_name] = {
                        "description": tool["instance"].get_method_description(method_name),
                        "signature": "(...)"
                    }
            
            tools_info.append(tool_info)
        
        return tools_info

    def scan_directory(self, directory: str) -> None:
        """Scan directory for tool files"""
        directory = Path(directory)
        if not directory.exists():
            print(f"Directory {directory} does not exist", file=sys.stderr)
            return

        # Iterate through first level subdirectories
        for tool_dir in directory.iterdir():
            if not tool_dir.is_dir():
                continue
                
            main_file = tool_dir / "main.py"
            if not main_file.exists():
                continue

            try:
                spec = importlib.util.spec_from_file_location(
                    "tool_module", str(main_file)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Only register classes that inherit from BaseTool
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (
                        inspect.isclass(item)
                        and issubclass(item, BaseTool)
                        and item != BaseTool
                        and not item.__name__.startswith('_')
                    ):
                        # Only register class, not filename
                        self.register_tool(item, str(main_file))
                        break  # Only register one tool class per file
            except Exception as e:
                print(f"load tool {main_file} error: {e}", file=sys.stderr)

