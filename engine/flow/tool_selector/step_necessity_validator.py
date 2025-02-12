from engine.flow.tool_selector.step_necessity_validator_prompt import (
    step_necessity_check_prompt,
)
from engine.llm_provider.llm import chat_completion
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")


def step_tool_check(plan, current_step, context, tools_and_outputs):
    prompt = step_necessity_check_prompt(
        plan, current_step, context, tools_and_outputs
    )
    result = chat_completion(
        prompt, model=PERFORMANCE_MODEL_NAME, config={"temperature": 0}
    )
    return result
