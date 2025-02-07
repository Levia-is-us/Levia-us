from typing import Any, Optional, Dict
import sys
import json
from .base_tool import BaseTool

class ToolRunner:
    """Tool runner that handles stdio communication"""
    def __init__(self, tool: BaseTool):
        self.tool = tool
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def _read_input(self) -> Optional[Dict]:
        """Read input from stdin"""
        try:
            input_data = self.stdin.readline().strip()
            if input_data:
                return json.loads(input_data)
            return None
        except Exception as e:
            self._write_error(f"Failed to parse input: {str(e)}")
            return None

    def _write_output(self, data: Any) -> None:
        """Write output to stdout"""
        try:
            output = json.dumps(data, ensure_ascii=False)
            self.stdout.buffer.write(output.encode('utf-8'))
            self.stdout.buffer.write(b'\n')
            self.stdout.buffer.flush()
        except Exception as e:
            self._write_error(f"Failed to write output: {str(e)}")

    def _write_error(self, error: str) -> None:
        """Write error to stderr"""
        try:
            error_data = json.dumps({"error": error}, ensure_ascii=False)
            self.stderr.buffer.write(error_data.encode('utf-8'))
            self.stderr.buffer.write(b'\n')
            self.stderr.buffer.flush()
        except Exception:
            pass

    def run(self) -> None:
        """Main run loop"""
        try:
            input_data = self._read_input()
            if not input_data:
                return

            if 'method' not in input_data:
                self._write_error("No method specified")
                return

            method_name = input_data['method']
            if method_name not in self.tool.methods:
                self._write_error(f"Method '{method_name}' not found")
                return

            method = self.tool.methods[method_name]
            args = input_data.get('args', {})

            try:
                result = method(**args)
                self._write_output({
                    "success": True,
                    "result": result
                })
            except Exception as e:
                self._write_error(f"Method execution failed: {str(e)}")

        except KeyboardInterrupt:
            return
        except Exception as e:
            self._write_error(f"Unexpected error: {str(e)}")