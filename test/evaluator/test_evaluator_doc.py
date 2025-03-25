import sys
import os

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
)

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from engine.flow.evaluator.evaluator_docgen_prompt import (
    create_evaluator_docgen_prompt,
)
from engine.llm_provider.llm import chat_completion
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def evaluator_docgen_flow(code, user_id):
    prompt = create_evaluator_docgen_prompt(code)
    result = chat_completion(
        prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0, "max_tokens": 4000}, user_id=user_id
    )
    return result


if __name__ == "__main__":

    code = """ code_file"""
    print(evaluator_docgen_flow(code, "local-dev"))
