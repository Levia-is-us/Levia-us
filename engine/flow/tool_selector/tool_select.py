from engine.flow.tool_selector.tool_select_prompt import tool_selector_prompt
from engine.llm_provider.llm import chat_completion
import json

def tool_select(plan, current_step, context, tools):
    prompt = tool_selector_prompt(plan, current_step, context, tools)
    result = chat_completion(prompt, model="o1-mini", config={"temperature": 0, "max_tokens": 4000})
    return result