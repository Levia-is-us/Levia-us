# Tool Development Documentation

## 1. File Path
- All developed tools must be stored in the `tools` folder.
- Each tool should have its own subfolder within the `tools` folder, named after the specific tool.
- Each tool's folder must include:
  - A `.env.example` file
  - A `requirements.txt` file
  - An entry file named `main.py`

## 2. Naming Rules
1. The main entry file must be named `main.py`.
2. The folder name should match the name of the main class in your `main.py`.
3. All methods, except the entry method, should be prefixed with an underscore (e.g., `_function_name`).
4. The entry method's name must clearly describe the tool’s functionality.
5. Variable names should be descriptive and reflect their content or purpose. Avoid arbitrary or meaningless names.

## 3. Entry Method Annotation
- The main class in `main.py` should be annotated with `@run_tool`, placed directly above the class definition.

## 4. Importing Tool Files
- When importing files from within a tool's folder, use the full path format. For example:
  `from tools.your_folder.your_file import your_method`

## `main.py` file example:
```
import os
import sys

# Set project root directory
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

# Import necessary tool framework components
from engine.tool_framework.tool_runner import ToolRunner
from engine.tool_framework import run_tool
from tools.your_folder.your_file import your_method

# Entry method with the @run_tool annotation
@run_tool
class ToolName:
    def your_tool_method(self):
        """Implement your tool's functionality here"""
        return your_output
```

## 5. Testing Your Tool
- Create a test.py file in your tool’s folder to test its functionality.
- The test.py file should be structured as follows (make sure to replace placeholders with your tool name and method):
```
import os
import sys
import dotenv

# Set project root directory
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Load environment variables
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

# Append the root project directory to the system path
sys.path.append(project_root)

# Import necessary components for tool testing
from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller

def main():
    # Initialize the tool registry and scan the tools directory
    registry = ToolRegistry()
    tools_dir = os.path.join(project_root, "tools")
    registry.scan_directory(tools_dir)

    # Initialize the tool caller and invoke the tool's method
    caller = ToolCaller(registry)
    result = caller.call_tool(
        tool_name="Your Tool Name",
        method="your_method_name",
        kwargs={
            "param1": "value1",
            "param2": "value2"
        }
    )

    print(result)

if __name__ == "__main__":
    main()
```

## 6. Additional Notes:
- Levia will automatically read your tool’s metadata and generate a tool registry document within your tool’s folder.
- The tool’s usage will then be stored in the database for easy access by the Levia engine.