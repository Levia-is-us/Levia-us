from engine.flow.handle_intent_flow.intents_system_prompt import intents_system_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
import os



def handle_intent_flow(chat_messages: list, input_message: str, user_id: str="local-dev", ch_id: str = "") -> dict:
    QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
    CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")
    """Get initial response from LLM"""
    prompt = intents_system_prompt(input_message)
    messages = chat_messages + prompt
    reply_info = chat_completion(
        messages, model=QUALITY_MODEL_NAME, config={"temperature": 0, "max_tokens": 4000}, user_id=user_id, ch_id=ch_id
    )
    result = extract_json_from_str(reply_info)
    # print(f"result: {result}")
    return result
