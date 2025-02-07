import sys
import os

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from checking_plan_prompt import check_plan_fittable_prompt
from engine.llm_provider.llm import chat_completion
from engine.flow.evaluator.evaluator_docgen_flow import extract_json_from_doc
import json

def check_plan_sufficiency(intent: str, plan_intent: str, execution_records: list) -> bool:
    """Check if existing plan is sufficient for current intent"""
    print(f"intent: {intent}")
    print(f"plan_intent: {plan_intent}")
    print(f"execution_records: {execution_records}")
    memories_check_prompt = [
        {"role": "assistant", "content": check_plan_fittable_prompt},
        {"role": "user", "content": f"Intent A: {intent}"},
        {"role": "user", "content": f"Intent B: {plan_intent}"},
        {"role": "user", "content": f"Proposed Solution: {execution_records}"}
    ]
    
    result = chat_completion(memories_check_prompt, model="deepseek-chat", 
                           config={"temperature": 0.7})
    print(f"result: {result}")
    print(f"type of result: {type(result)}")
    try:
        result = json.loads(result)
    except:
        result = extract_json_from_doc(result)
    
    return result

if __name__ == "__main__":
    """put your intent, plan_intent, execution_records here"""
    intent = "user intent"
    plan_intent = "plan intent"
    execution_records = "execution records"
    result = check_plan_sufficiency(intent, plan_intent, execution_records)
    print(f"result: {result}")

