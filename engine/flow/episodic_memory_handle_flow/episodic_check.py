from engine.flow.episodic_memory_handle_flow.episodic_check_prompt import episodic_check_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
import os
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def episodic_check(user_intent, context, plan):
    prompt = episodic_check_prompt(user_intent, context, plan)
    result = chat_completion(prompt, QUALITY_MODEL_NAME, config={"temperature": 0})
    start_tag = "<think>"
    end_tag = "</think>"
    start_index = result.find(start_tag)
    end_index = result.find(end_tag)
    if start_index != -1 and end_index != -1 and end_index > start_index:
        result = result[:start_index] + result[end_index + len(end_tag):]
    try:
        result = extract_json_from_str(result)
        print(f"episodic_check result: {result}")
    except:
        massage = "wrong format of episodic_check result: " + result
        raise Exception(massage)
    return result

