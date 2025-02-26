from engine.flow.evaluator.evaluator_docgen_prompt import (
    system_prompt,
    prompt
)
from engine.llm_provider.llm import create_chat_completion
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def evaluator_docgen_flow(code):
    result = create_chat_completion(
        system_prompt = system_prompt,
        prompt = prompt.replace("{{PYTHON_CODE}}", code),
        model=QUALITY_MODEL_NAME,
        config={"temperature": 0, "max_tokens":8000},
        user_id="local-dev",
        ch_id=""
    )
    return result
