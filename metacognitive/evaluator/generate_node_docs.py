# generate node docs
# 1. get all folder in side root/nodes
# 2. for each folder, get main.py python file
# 3. use llm to generate the guideline for each node
# 4. save the docstring to a new file in root/nodes/folder_name/docs.md
import json
import os
import sys


# Add project root directory to Python path
project_root = ""

if __name__ == "__main__":
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    sys.path.append(project_root)

else:
    project_root = os.path.dirname(os.path.abspath(__file__))

node_path = os.path.join(project_root, "tools")
print(node_path)

from memory.episodic_memory.episodic_memory import store_short_pass_memory
from engine.flow.evaluator.evaluator_docgen_flow import evaluator_docgen_flow
from engine.utils.json_util import (
    extract_json_from_str,
    extract_code_breakdown_from_doc,
)

for folder in os.listdir(node_path):
    if os.path.isdir(os.path.join(node_path, folder)):
        print(folder)
        main_file = os.path.join(node_path, folder, "main.py")
        if os.path.exists(main_file) and not os.path.exists(
            os.path.join(node_path, folder, "docs.md")
        ):
            print(main_file)
            with open(main_file, "r") as f:
                content = f.read()
                doc = evaluator_docgen_flow(content)
                # save doc to a new file in root/nodes/folder_name/docs.md
                with open(os.path.join(node_path, folder, "docs.md"), "w") as f:
                    f.write(doc)

                json_data = extract_json_from_str(doc)
                code_breakdown = extract_code_breakdown_from_doc(doc)

                for function in json_data["functions"]:
                    detailed_description = function.pop("detailed_description")
                    short_description = function.pop("short_description")
                    metadata = {
                        "method": function["method"],
                        "tool": function["method"] + "_tool",
                        "data": json.dumps(function),
                        "short_description": short_description,
                        "description": code_breakdown,
                        "details": detailed_description,
                    }

                    store_short_pass_memory(
                        folder + "-" + function["method"], short_description, metadata
                    )
