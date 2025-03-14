from engine.flow.handle_reply_flow.final_reply_prompt import final_reply_prompt
import os
from metacognitive.stream.stream import output_stream
from engine.llm_provider.llm import chat_completion


QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")


def handle_reply_flow(
    chat_messages: list, engine_output: list, user_id: str, ch_id: str = ""
) -> str:
    """Handle final reply type response"""
    CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")
    output_stream(
        log="Considering the reply...", user_id=user_id, type="steps", ch_id=ch_id
    )
    prompt = final_reply_prompt(chat_messages, engine_output)
    print("engine_output", engine_output)
    final_reply = chat_completion(
        prompt,
        model=CHAT_MODEL_NAME,
        config={"temperature": 0.7},
        user_id=user_id,
        ch_id=ch_id,
    )
    if final_reply == None or final_reply == "":
        raise Exception("Final reply is None")

    return final_reply
