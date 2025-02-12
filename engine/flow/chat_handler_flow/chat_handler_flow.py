from engine.flow.chat_handler_flow.intents_system_prompt import intents_system_prompt
from engine.llm_provider.llm import chat_completion
from memory.episodic_memory.episodic_memory import retrieve_long_pass_memory
from engine.utils.json_util import extract_json_from_str
from engine.flow.executor.chat_executor import process_existing_memories
from engine.flow.executor.chat_executor import filter_high_score_memories
from engine.flow.chat_handler_flow.final_reply_prompt import final_reply_prompt
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")


def handle_chat_flow(chat_messages: list, user_input: str, tool_caller, user_id: str) -> str:
    """Handle the main chat flow logic"""
    # Get initial response
    reply_info = get_initial_response(chat_messages)
    print(f"reply_info: {reply_info}")

    # Handle different response types
    if reply_info["type"] == "direct_answer":
        message_copy = chat_messages.copy()
        message_copy.append({"role": "assistant", "content": f"{reply_info}"})
        final_reply = handle_final_reply(message_copy)
        return final_reply
    elif reply_info["type"] == "intent":
        handle_intent_summary(reply_info, chat_messages, tool_caller)
        final_reply = handle_final_reply(chat_messages)
        chat_messages.append({"role": "assistant", "content": f"{final_reply}"})
        return final_reply
    elif reply_info["type"] == "input-intent":
        handle_input_intent(reply_info, chat_messages, tool_caller, user_id)



def get_initial_response(chat_messages: list) -> dict:
    """Get initial response from LLM"""
    prompt = intents_system_prompt(chat_messages)
    reply_info = chat_completion(
        prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0}
    )
    return extract_json_from_str(reply_info)


def handle_final_reply(chat_messages: list) -> str:
    """Handle final reply type response"""
    prompt = final_reply_prompt(chat_messages)
    final_reply = chat_completion(
        prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0.7}
    )

    return final_reply


def handle_intent_summary(reply_info: dict, chat_messages: list, tool_caller) -> str:
    """Handle intent summary type response"""
    user_intent = reply_info["user_intent"]
    execution_records_str = []

    memories = retrieve_long_pass_memory(user_intent)
    high_score_memories = filter_high_score_memories(memories)

    return process_existing_memories(
        high_score_memories,
        user_intent,
        execution_records_str,
        chat_messages,
        tool_caller,
    )

def handle_input_intent(reply_info: dict, chat_messages: list, tool_caller, user_id: str) -> str:
    """Handle intent summary type response"""
    user_intent = reply_info["user_intent"]
    execution_records_str = []

    memories = retrieve_long_pass_memory(user_intent)
    high_score_memories = filter_high_score_memories(memories)

    return process_existing_memories(
        high_score_memories,
        user_intent,
        execution_records_str,
        chat_messages,
        tool_caller,
    )
