from engine.flow.tool_selector.step_necessity_validator_prompt import (
    step_necessity_check_prompt,
)
from engine.llm_provider.llm import chat_completion
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def step_tool_check(plan, current_step, context, tools_and_outputs, user_id):
    prompt = step_necessity_check_prompt(
        plan, current_step, context, tools_and_outputs
    )
    result = chat_completion(
        prompt, model=CHAT_MODEL_NAME, config={"temperature": 0, "max_tokens": 4000}, user_id=user_id
    )
    return result
