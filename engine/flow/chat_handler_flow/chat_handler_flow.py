from engine.flow.handle_intent_flow.analyze_intent_flow import handle_intent_flow
from engine.flow.handle_reply_flow.generate_reply_flow import handle_reply_flow
from engine.utils.chat_formatter import create_chat_message
from engine.utils.json_util import (
    extract_code_breakdown_from_doc,
    extract_str_from_doc,
)
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.flow.executor.chat_executor_flow import chat_executor
import os

from metacognitive.stream.stream import output_stream
from memory.plan_memory.plan_memory import PlanContextMemory
from engine.flow.executor.execute_short_chain_flow import process_plan_execution

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

short_term_memory = ShortTermMemory()
plan_context_memory = PlanContextMemory()


def handle_chat_flow(user_input: str, user_id: str, chid: str, session_id: str = "") -> str:
    """Handle the main chat flow logic"""
    # Get initial response
    chat_messages = short_term_memory.get_context(user_id + session_id)[-6:]
    output_stream(log="Analyzing user's intent ...", user_id=user_id, type="steps", ch_id=chid)
    reply_info = handle_intent_flow(chat_messages, user_input, user_id, chid)
    short_term_memory.add_context(
        create_chat_message("user", user_input), user_id + session_id
    )
    chat_messages = short_term_memory.get_context(user_id + session_id)[-7:]
    output_stream(log=f"user intent: {reply_info['intent']}", user_id=user_id, type="think", ch_id=chid)
    
    final_reply = ""
    # Handle different response types
    if reply_info["type"] == "direct_answer":
        response = reply_info["response"]
        final_reply = handle_reply_flow(chat_messages, [{"normal_llm_reply": response}], user_id, chid)
    elif reply_info["type"] == "call_tools":
        plan_result = handle_intent_summary(reply_info, chat_messages, user_id, chid)
        # print(f"plan_result: {plan_result}")
        final_reply = handle_reply_flow(chat_messages, plan_result, user_id, chid)
        
    elif reply_info["type"] == "continue_execution":
        plan_result = handle_input_intent(chat_messages, user_id, chid)
        final_reply = handle_reply_flow(chat_messages, plan_result, user_id, chid)
        
    # final_reply = extract_str_from_doc(final_reply)
    short_term_memory.add_context(
        create_chat_message("assistant", f"{final_reply}"), user_id + session_id
    )
    output_stream(log=f"{final_reply}", user_id=user_id, type="think", ch_id=chid, title="Final reply")
    return final_reply


def handle_intent_summary(reply_info: dict, chat_messages: list, user_id: str, chid: str):
    """Handle intent summary type response"""
    user_intent = reply_info["intent"]
    return chat_executor(user_id, user_intent, chat_messages, chid)
    


def handle_input_intent(chat_messages, user_id: str, chid: str) -> str:
    """Handle intent summary type response"""
    chat_messages = short_term_memory.get_context(user_id)
    plan_context = plan_context_memory.get_current_plan_context(user_id)
    return process_plan_execution(chat_messages, plan_context, user_id=user_id, ch_id=chid)
