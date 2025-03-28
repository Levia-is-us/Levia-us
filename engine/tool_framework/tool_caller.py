from typing import Optional, Dict, List, Any
from .tool_registry import ToolRegistry
import sys
import threading
import _thread
import atexit
import gc

class TimeoutException(Exception):
    pass

class ToolCaller:
    """Class for calling tools"""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def _cleanup_resources(self):
        """Clean up resources"""
        # Force garbage collection
        gc.collect()
        
        # Try to close resources in current tool instance
        if hasattr(self.registry, 'tools'):
            for tool_info in self.registry.tools.values():
                tool_instance = tool_info.get('instance')
                if tool_instance:
                    # Call cleanup method if exists
                    if hasattr(tool_instance, 'cleanup'):
                        try:
                            tool_instance.cleanup()
                        except:
                            pass
                    # Call quit method if exists
                    elif hasattr(tool_instance, 'quit'):
                        try:
                            tool_instance.quit()
                        except:
                            pass
                    # Call close method if exists
                    elif hasattr(tool_instance, 'close'):
                        try:
                            tool_instance.close()
                        except:
                            pass

    def _run_with_timeout(self, method, timeout: int, **kwargs):
        """Run method with timeout using thread"""
        def raise_timeout():
            self._cleanup_resources()  # Clean up before timeout
            _thread.interrupt_main()
        timer = threading.Timer(timeout, raise_timeout)
        timer.start()
        
        try:
            result = method(**kwargs) if kwargs else method()
            return result
        except KeyboardInterrupt:
            self._cleanup_resources()  # Clean up on timeout
            raise TimeoutException(f"Tool execution timed out after {timeout} seconds")
        finally:
            timer.cancel()
            self._cleanup_resources()  # Ensure cleanup

    def call_tool(self, tool_name: str, method: str, kwargs: dict = None):
        """Call a tool method"""
        try:
            # Get tool instance
            tool_info = self.registry.get_tool(tool_name)
            if not tool_info:
                return {"error": f"Tool '{tool_name}' not found"}

            # Get instance from tool info
            tool_instance = tool_info["instance"]
            
            # Get method
            tool_method = getattr(tool_instance, method, None)
            if not tool_method:
                return {"error": f"Method '{method}' not found in tool '{tool_name}'"}

            # Get timeout value from tool instance
            timeout = getattr(tool_instance, 'timeout', 180)  # Default 180 seconds

            try:
                # Execute method with timeout
                result = self._run_with_timeout(tool_method, timeout, **(kwargs or {}))
                return result
            except TimeoutException as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": str(e)}

        except Exception as e:
            return {"error": str(e)}

        finally:
            self._cleanup_resources()  # Ensure final cleanup

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return self.registry.list_tools()