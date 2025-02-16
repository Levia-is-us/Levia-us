from engine.flow.planner.planner_prompt import get_plan_maker_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
from engine.flow.planner.checking_plan_prompt import check_plan_fittable_prompt
from metacognitive.stream.stream import output_stream
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")


def create_execution_plan(intent: str) -> str:
    """Create execution plan for given intent summary"""
    plan_maker_prompt = get_plan_maker_prompt(intent)
    prompt = [
        {"role": "user", "content": plan_maker_prompt},
    ]
    plan = chat_completion(
        prompt, model=PERFORMANCE_MODEL_NAME, config={"temperature": 0.5}
    )
    plan = extract_json_from_str(plan)
    for step in plan:
        output_stream(f" - {step['step']}: {step['intent']} - \n")
        output_stream(f" - Step Description: {step['description']} - \n")
        output_stream(f" - Step Reason: {step['reason']} - \n")
        output_stream(f"\033[95m--------------------------------\033[0m")
    return plan


def check_plan_sufficiency(
    intent: str, plan_intent: str, execution_records: list
) -> bool:
    """Check if existing plan is sufficient for current intent"""
    # print(f"intent: {intent}")
    # print(f"plan: {plan_intent}")
    # print(f"execution_records: {execution_records}")
    memories_check_prompt = check_plan_fittable_prompt(
        intent, plan_intent, execution_records
    )

    result = chat_completion(
        memories_check_prompt, model=PERFORMANCE_MODEL_NAME, config={"temperature": 0}
    )
    result = extract_json_from_str(result)
    # print(f"result: {result}")
    # print(f"type of result: {type(result)}")

    return result["solution_sufficient"]["result"] in [True, "true"]
