import sys
from engine.tool_framework.tool_runner import ToolRunner

def run_tool(description=""):
    """Decorator to run a tool"""
    def decorator(cls):
        # If a string is passed, this is the description
        if isinstance(description, str):
            cls.__doc__ = description or cls.__doc__
            return cls
        # If a class is passed, no description is provided
        tool_class = description
        tool_class.__doc__ = tool_class.__doc__ or "No description available"
        return tool_class
    
    # If the decorator has no parameters, return the class decorator
    if isinstance(description, type):
        return decorator(description)
    # Otherwise return decorator with parameters
    return decorator