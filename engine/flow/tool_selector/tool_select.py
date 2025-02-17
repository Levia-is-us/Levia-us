from engine.flow.tool_selector.tool_select_prompt import tool_selector_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def tool_select(plan, current_step, context, tools):
    prompt = tool_selector_prompt(plan, current_step, context, tools)
    result = chat_completion(
        prompt, model=CHAT_MODEL_NAME, config={"temperature": 0, "max_tokens": 4000}
    )
    result = extract_json_from_str(result)
    # print(f"Tool selection result: {result}")
    tool_name = result.get("tool_name", "Tool not found")

    return tool_name