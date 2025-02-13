from typing import Optional, Dict
from .tool_registry import ToolRegistry
import subprocess
import json
import sys
import os


class ToolCaller:
    """Class for calling tools"""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def call_tool(self, tool_name: str, method: str, kwargs: Dict) -> Optional[Dict]:
        """Call a specific tool method"""
        tool_path = self.registry.get_tool_path(tool_name)
        if not tool_path:
            raise ValueError(f"Tool '{tool_name}' not found")

        # Start tool process
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.dirname(os.path.dirname(tool_path))
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.Popen(
            [sys.executable, tool_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            text=True,
            bufsize=1,
            env=env,
        )

        # Prepare input data
        input_data = {"method": method, "args": kwargs}

        # Send input and get output with timeout
        stdout, stderr = process.communicate(
            json.dumps(input_data, ensure_ascii=False) + "\n",
            timeout=600,  # Add timeout
        )

        if stderr and not stdout:
            print(f"Tool stderr: {stderr}", file=sys.stderr)
            return None

        if not stdout:
            return None
        
        try:
            result = json.loads(stdout.strip())
            return (
                result.get("result")
                if isinstance(result, dict) and "result" in result
                else result
            )
        except json.JSONDecodeError:
            print(f"Failed to parse tool output: {stdout!r}", file=sys.stderr)
            return {"status": "failure", "result": "Failed to parse tool output"}
        except subprocess.TimeoutExpired:
            process.kill()
            print("Tool execution timed out", file=sys.stderr)
            return {"status": "failure", "result": "Tool execution timed out"}
        except Exception as e:
            print(f"Error calling tool: {str(e)}", file=sys.stderr)
            return {"status": "failure", "result": str(e)}
