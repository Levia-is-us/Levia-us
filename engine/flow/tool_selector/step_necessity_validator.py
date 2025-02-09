from engine.flow.tool_selector.step_necessity_validator_prompt import step_necessarity_check_prompt
from engine.llm_provider.llm import chat_completion
import json

def step_tool_check(plan, current_step, context, tools_and_outputs):
    prompt = step_necessarity_check_prompt(plan, current_step, context, tools_and_outputs)
    result = chat_completion(prompt, model="o1-mini", config={"temperature": 0, "max_tokens": 4000})
    return result