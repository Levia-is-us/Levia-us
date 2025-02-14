from engine.flow.handle_reply_flow.final_reply_prompt import final_reply_prompt
import os

from engine.llm_provider.llm import chat_completion

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")


def handle_reply_flow(chat_messages: list, execution_context: list) -> str:
    """Handle final reply type response"""
    prompt = final_reply_prompt(execution_context)
    chat_messages.append(prompt)
    final_reply = chat_completion(
        chat_messages, model=QUALITY_MODEL_NAME, config={"temperature": 0.7}
    )

    return final_reply
