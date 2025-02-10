from engine.flow.tool_selector.tool_select_prompt import tool_selector_prompt
from engine.llm_provider.llm import chat_completion
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
FAST_MODEL_NAME = os.getenv("FAST_MODEL_NAME")


def tool_select(plan, current_step, context, tools):
    prompt = tool_selector_prompt(plan, current_step, context, tools)
    result = chat_completion(
        prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0, "max_tokens": 4000}
    )
    return result
