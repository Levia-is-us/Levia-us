from engine.flow.handle_intent_flow.handle_intent_flow import handle_intent_flow
from engine.flow.handle_reply_flow.handle_reply_flow import handle_reply_flow
from engine.utils.chat_formatter import create_chat_message
from memory.episodic_memory.episodic_memory import retrieve_long_pass_memory
from engine.flow.executor.chat_executor import process_existing_memories
from engine.flow.executor.chat_executor import filter_high_score_memories
from memory.short_term_memory.short_term_memory import ShortTermMemory
import os

from metacognitive.stream.stream import output_stream


QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")

short_term_memory = ShortTermMemory()


def handle_chat_flow(chat_messages: list, user_input: str, tool_caller) -> str:
    """Handle the main chat flow logic"""
    # Get initial response
    chat_messages = short_term_memory.get_context()
    reply_info = handle_intent_flow(chat_messages, user_input)
    output_stream(f"{reply_info['intent']}")

    # Handle different response types
    if reply_info["type"] == "direct_answer":
        response = reply_info["response"]
        short_term_memory.add_context(
            [
                create_chat_message("user", user_input),
                create_chat_message("assistant", f"{response}"),
            ]
        )
        return response

    elif reply_info["type"] == "call_tools":
        handle_intent_summary(reply_info, chat_messages, tool_caller)
        final_reply = handle_reply_flow(chat_messages)
        short_term_memory.add_context(
            [
                create_chat_message("user", user_input),
                create_chat_message("assistant", f"{final_reply}"),
            ]
        )
        return final_reply


def handle_intent_summary(reply_info: dict, chat_messages: list, tool_caller) -> str:
    """Handle intent summary type response"""
    user_intent = reply_info["response"]
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
