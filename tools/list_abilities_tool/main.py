import json
import os
import sys
from dotenv import load_dotenv


project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)
sys.path.append(project_root)

from engine.tool_framework import simple_tool
from engine.tool_framework.tool_runner import ToolRunner
from engine.utils.json_util import extract_json_from_str


@simple_tool("Tool for listing available abilities")
def list_abilities():
    tools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abilities = []

    # Walk through all directories in tools folder
    for root, dirs, files in os.walk(tools_dir):
        if "docs.md" in files:
            docs_path = os.path.join(root, "docs.md")
            try:
                with open(docs_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    json_strs = extract_json_from_str(content)
                    for json_str in json_strs["functions"]:
                        abilities.append(
                            {
                                "method": json_str["method"],
                                "description": json_str["short_description"],
                            }
                        )

            except json.JSONDecodeError:
                continue

            except Exception as e:
                print(f"Error processing {docs_path}: {str(e)}", file=sys.stderr)
                continue

    return abilities


def main():
    tool = list_abilities()
    runner = ToolRunner(tool)
    runner.run()


if __name__ == "__main__":
    main()
