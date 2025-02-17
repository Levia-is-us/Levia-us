from engine.llm_provider.llm import chat_completion
from engine.flow.planner.tool_base_planner_prompt import get_tool_base_planner_prompt
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def tool_base_planner(intent: str, tool_list: list):
    tool_base_planner_prompt = get_tool_base_planner_prompt(intent, tool_list)
    prompt = [
        {"role": "user", "content": tool_base_planner_prompt},
    ]
    plan = chat_completion(prompt, model=CHAT_MODEL_NAME, config={"temperature": 0.5})
    return plan
