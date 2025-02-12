# Tool Development Documentation

## 1. File Path
- All developed tools should be stored in the `tools` folder.
- Each tool must have its own subfolder within the `tools` folder, with each subfolder corresponding to a specific tool.

## 2. Naming Rules
1. The main entry file of the tool must be named `main.py`.
2. The folder name for each tool should be the entry method name + "_tool".
3. The entry method's name should accurately describe the tool's functionality.
4. Variable names should reflect their content or function. Avoid using arbitrary or meaningless names.

## 3. Entry Method Annotation
- Above the entry method, the following annotation must be added: `@simple_tool("Tool Overview")`.

## 4. Tool Registration
- In the `main.py` file, the tool registration file should be imported, and the `main()` method should be called at the end to register the tool.

## 5. Importing Tool Files
- When importing files from within a tool's folder, you must use the full path, for example: from tools.your_folder.your_file import your_method

## Example
```
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from engine.tool_framework.tool_runner import ToolRunner
from engine.tool_framework import simple_tool
from tools.your_folder.your_file import your_method

@simple_tool("Tool Overview")
def your_tool_method():
    """Implement your tool's functionality here"""
    return your_output

def main():
    # Create tool instance
    tool = save_markdown_to_gitbook()  # Get tool instance directly
    runner = ToolRunner(tool)
    runner.run()

if __name__ == "__main__":
    main()
```

## 6. Dependency Management
- Each tool's folder must include a requirements.txt file. If necessary, you may configure a local environment within the tool folder and provide an example.

## 7. Third-Party API
- If a tool calls a third-party API, only publicly available and trusted APIs are supported. Private APIs are not supported.
