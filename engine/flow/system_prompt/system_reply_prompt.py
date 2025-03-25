from engine.llm_provider.llm import get_model_by_name
from engine.utils.chat_formatter import create_chat_message
import os

CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
final_system_prompt = """Your name is Levia, and you are an AI strategist in a Living Agent Ecosystem, help user to do running tasks and answer questions. Your task is to modify the engine's responses to make them more suitable for a social media or chat environment.
"""


def get_system_reply_prompt():
    model = get_model_by_name(QUALITY_MODEL_NAME)
    if not model:
        raise ValueError(f"Model {QUALITY_MODEL_NAME} not found")

    system_prompt = ""
    if model["type"] == "reasoning":
        if model["source"] == "openai":
            system_prompt = get_system_reply_prompt_for_openai_reasoning()
        elif model["source"] == "anthropic":
            system_prompt = get_system_reply_prompt_for_anthropic_reasoning()
        elif model["source"] == "deepseek":
            system_prompt = get_system_reply_prompt_for_deepseek_reasoning()
    else:
        system_prompt = create_chat_message("system", final_system_prompt)
    return system_prompt


def get_system_reply_prompt_for_openai_reasoning():
    return create_chat_message("developer", final_system_prompt)


def get_system_reply_prompt_for_anthropic_reasoning():
    return create_chat_message("assistant", final_system_prompt)


def get_system_reply_prompt_for_deepseek_reasoning():
    return create_chat_message("assistant", final_system_prompt)
