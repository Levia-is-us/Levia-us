from engine.flow.handle_intent_flow.handle_intent_flow import handle_intent_flow
from engine.flow.handle_reply_flow.handle_reply_flow import handle_reply_flow
from engine.utils.chat_formatter import create_chat_message
from engine.utils.json_util import (
    extract_code_breakdown_from_doc,
    extract_json_from_str,
    extract_str_from_doc,
)
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.flow.executor.chat_executor import chat_executor
import os

from metacognitive.stream.stream import output_stream
from memory.plan_memory.plan_memory import PlanContextMemory
from engine.flow.executor.short_chain_executor import execute_intent_chain

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

short_term_memory = ShortTermMemory()
plan_context_memory = PlanContextMemory()


def handle_chat_flow(user_input: str, user_id: str) -> str:
    """Handle the main chat flow logic"""
    # Get initial response

    chat_messages = short_term_memory.get_context(user_id)
    print("\033[93mThinking about user's intent...\033[0m")
    reply_info = handle_intent_flow(chat_messages, user_input)
    output_stream(f"{reply_info['intent']}")
    short_term_memory.add_context(
        create_chat_message("user", user_input), user_id
    )
    chat_messages.append(create_chat_message("user", user_input))
    final_reply = ""
    # Handle different response types
    if reply_info["type"] == "direct_answer":
        response = reply_info["response"]
        print("\033[93mGenerating reply...\033[0m")
        final_reply = handle_reply_flow(chat_messages, [{"normal_llm_reply": response}])
        short_term_memory.add_context(
            create_chat_message("assistant", f"{final_reply}"), user_id
        )
    elif reply_info["type"] == "call_tools":
        plan_result = handle_intent_summary(reply_info, chat_messages, user_id)
        final_reply = handle_reply_flow(chat_messages, plan_result)
        short_term_memory.add_context(
            create_chat_message("assistant", f"{final_reply}"), user_id
        )
    elif reply_info["type"] == "continue_execution":
        plan_result = handle_input_intent(user_id)
        final_reply = handle_reply_flow(chat_messages, plan_result)
        short_term_memory.add_context(
            create_chat_message("assistant", f"{final_reply}"), user_id
        )
        return final_reply

    analysis = extract_code_breakdown_from_doc(final_reply)
    output_stream(f"{analysis}")
    final_reply = extract_str_from_doc(final_reply)

    return final_reply


def handle_intent_summary(reply_info: dict, chat_messages: list, user_id: str):
    """Handle intent summary type response"""
    user_intent = reply_info["response"]
    return chat_executor(user_id, user_intent, chat_messages)
    


def handle_input_intent(user_id: str) -> str:
    """Handle intent summary type response"""
    chat_messages = short_term_memory.get_context(user_id)
    plan_context = plan_context_memory.get_current_plan_context(user_id)
    return execute_intent_chain(
        chat_messages=chat_messages, plan_steps=plan_context, user_id=user_id
    )
