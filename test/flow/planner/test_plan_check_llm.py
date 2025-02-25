import sys
import os

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from engine.flow.planner.checking_plan_prompt import check_plan_fittable_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
import json

def check_plan_sufficiency(intent: str, plan_intent: str, execution_records: list) -> bool:
    """Check if existing plan is sufficient for current intent"""
    print(f"intent: {intent}")
    print(f"plan_intent: {plan_intent}")
    print(f"execution_records: {execution_records}")
    memories_check_prompt = check_plan_fittable_prompt(intent, plan_intent, execution_records)
    
    result = chat_completion(memories_check_prompt, model="deepseek-chat", 
                           config={"temperature": 0.7})
    print(f"result: {result}")
    print(f"type of result: {type(result)}")
    try:
        result = json.loads(result)
    except:
        result = extract_json_from_str(result)
    
    return result

if __name__ == "__main__":
    """put your intent, plan_intent, execution_records here"""
    intent = "get football news"
    plan_intent = "The user wants to search for today's football news."
    execution_records = [{
        "step 1": "Data Extraction Tool",
        "Description": "Use a web scraping or API-based tool to extract today's football news from reliable sources such as sports news websites or APIs.",

        "Reason": "To gather up-to-date and accurate information about today's football news from trusted sources."
    },
    {
        "step 2": "Data Filtering and Organization Tool",
        "Description": "Filter and organize the extracted news data to remove duplicates, irrelevant content, or low-quality sources, ensuring only meaningful and relevant news is retained.",
        "Reason": "To ensure the user receives concise, high-quality, and relevant football news without unnecessary clutter."
    },
    {
        "step 3": "Knowledge Documentation Generation and Upload",
        "Description": "Utilize the tool that generates documentation and uploads to GitBook to compile all useful and meaningful knowledge produced during the plan's execution into a document and upload it to GitBook, ensuring long-term preservation and reuse of valuable information.",
        "Reason": "To document and preserve the curated football news for future reference or learning purposes, ensuring the information remains accessible and reusable."
    }
]
    result = check_plan_sufficiency(intent, plan_intent, execution_records)
    print(f"result: {result}")

