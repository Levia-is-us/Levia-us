from engine.flow.planner.planner_prompt import get_plan_maker_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
from engine.flow.planner.checking_plan_prompt import check_plan_fittable_prompt
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
        prompt, model=CHAT_MODEL_NAME, config={"temperature": 0.5}, user_id=user_id, ch_id=ch_id
    )
    plan = extract_json_from_str(plan)
    for step in plan:
        output_stream(log=f" - {step['step']}: {step['intent']} - \n - Step Description: {step['description']} - \n - Step Reason: {step['reason']}", user_id=user_id, type="think", ch_id=ch_id)
    return plan


def check_plan_sufficiency(
    intent: str, plan_intent: str, execution_records: list, user_id: str, ch_id: str = ""
) -> bool:
    """Check if existing plan is sufficient for current intent"""
    memories_check_prompt = check_plan_fittable_prompt(
        intent, plan_intent, execution_records
    )

    result = chat_completion(
        memories_check_prompt, model=CHAT_MODEL_NAME, config={"temperature": 0}, user_id=user_id, ch_id=ch_id
    )
    result = extract_json_from_str(result)
    return result["solution_sufficient"]["result"] in [True, "true"]
