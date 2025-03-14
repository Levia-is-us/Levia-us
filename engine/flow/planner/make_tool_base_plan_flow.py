from engine.llm_provider.llm import chat_completion
from engine.flow.planner.tool_base_planner_prompt import get_tool_base_planner_prompt
import os
from engine.utils.json_util import extract_json_from_str


def tool_base_planner(
    intent: str, tool_list: list, user_id: str, ch_id: str, context: list
):
    QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
    tool_base_planner_prompt = get_tool_base_planner_prompt(intent, tool_list, context)
    prompt = [
        {"role": "user", "content": tool_base_planner_prompt},
    ]
    plan = chat_completion(
        prompt,
        model=QUALITY_MODEL_NAME,
        config={"temperature": 0.7, "max_tokens": 4000},
        user_id=user_id,
        ch_id=ch_id,
    )
    plan = extract_json_from_str(plan)
    print(f"plan: {plan}")
    return plan
