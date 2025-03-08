from engine.flow.planner.planner_prompt import get_plan_maker_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
from metacognitive.stream.stream import output_stream
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def create_execution_plan(intent: str, user_id: str, ch_id: str = "") -> str:
    """Create execution plan for given intent summary"""
    plan_maker_prompt = get_plan_maker_prompt(intent)
    prompt = [
        {"role": "user", "content": plan_maker_prompt},
    ]
    plan = chat_completion(
        prompt, model=CHAT_MODEL_NAME, config={"temperature": 0.5, "max_tokens": 2000}, user_id=user_id, ch_id=ch_id
    )
    plan = extract_json_from_str(plan)
    log_str = ""
    for step in plan:
        log_str += f" {step['intent']} - \n - Step Description: {step['description']} - \n - Step Reason: {step['reason']}\n"
    output_stream(log=log_str, user_id=user_id, type="think", ch_id=ch_id)
    return plan
