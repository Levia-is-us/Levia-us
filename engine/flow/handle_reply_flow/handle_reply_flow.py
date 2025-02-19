from engine.flow.handle_reply_flow.final_reply_prompt import final_reply_prompt
import os
from metacognitive.stream.stream import output_stream
from engine.llm_provider.llm import chat_completion


QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def handle_reply_flow(chat_messages: list, engine_output: list) -> str:
    """Handle final reply type response"""
    output_stream(f"**Considering the reply...**")
    prompt = final_reply_prompt(chat_messages, engine_output)
    final_reply = chat_completion(
        prompt, model=CHAT_MODEL_NAME, config={"temperature": 0.7}
    )

    return final_reply
