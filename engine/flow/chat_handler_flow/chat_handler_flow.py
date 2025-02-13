from engine.flow.handle_intent_flow.handle_intent_flow import handle_intent_flow
from engine.flow.handle_reply_flow.handle_reply_flow import handle_reply_flow
from engine.utils.chat_formatter import create_chat_message
from engine.utils.memory_filter import filter_memories_by_score
from memory.episodic_memory.episodic_memory import retrieve_long_pass_memory
from engine.flow.executor.chat_executor import process_existing_memories
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.flow.executor.chat_executor import execute_plan_steps
import os

from metacognitive.stream.stream import output_stream
from memory.plan_memory.plan_memory import PlanContextMemory

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")

short_term_memory = ShortTermMemory()
plan_context_memory = PlanContextMemory()


def handle_chat_flow(user_input: str, user_id: str) -> str:
    """Handle the main chat flow logic"""
    # Get initial response

    chat_messages = short_term_memory.get_context(user_id)
    reply_info = handle_intent_flow(chat_messages, user_input)
    output_stream(f"{reply_info['intent']}")
    short_term_memory.add_context(create_chat_message("user", user_input), user_id)

    # Handle different response types
    if reply_info["type"] == "direct_answer":
        response = reply_info["response"]
        short_term_memory.add_context(
            create_chat_message("assistant", f"{response}"), user_id
        )
        return response
    elif reply_info["type"] == "call_tools":
        plan_result = handle_intent_summary(reply_info, chat_messages, user_id)
        final_reply = handle_reply_flow(chat_messages)
        short_term_memory.add_context(
            create_chat_message("assistant", f"{final_reply}"), user_id
        )
        return final_reply
    elif reply_info["type"] == "input-intent":
        handle_input_intent(user_id)


def handle_intent_summary(reply_info: dict, chat_messages: list, user_id: str):
    """Handle intent summary type response"""
    user_intent = reply_info["response"]
    memories = retrieve_long_pass_memory(user_intent)
    high_score_memories = filter_memories_by_score(memories)

    return process_existing_memories(
        high_score_memories, user_intent, chat_messages, user_id
    )


def handle_input_intent(user_id: str) -> str:
    """Handle intent summary type response"""
    chat_messages = short_term_memory.get_context(user_id)
    plan_context = plan_context_memory.get_current_plan_context(user_id)
    execute_plan_steps(
        plan_steps=plan_context, chat_messages=chat_messages, user_id=user_id
    )
