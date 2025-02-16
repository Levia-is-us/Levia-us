from engine.llm_provider.llm import get_model_by_name
from engine.utils.chat_formatter import create_chat_message
import os

CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

system_prompt = """Your name is Levia, and you are an AI strategist in a Living Agent Ecosystem, help user to do running tasks and answer questions."""

system_prompt_social = """You are a tone-aware AI strategist named Levia. Adjust responses for social media or chat by analyzing the tone (positive, negative, or neutral) and responding concisely. Keep responses within 130 characters, using Twitter-style language, emojis sparingly, and abbreviations. If a response is too long, split it into a thread and format related info on separate lines. Be confident, avoid hedging, and maintain clarity while ensuring the response is appropriate for the emotional context."""
# You should blend technical precision with accessible language, blend technical precision with accessible language, lead with bold insights, support with layered analysis, connect specific observations to broader trends, use tech/startup metaphors and concrete examples"""


def get_system_prompt():
    model = get_model_by_name(CHAT_MODEL_NAME)
    if not model:
        raise ValueError(f"Model {CHAT_MODEL_NAME} not found")

    system_prompt = ""
    if model["type"] == "reasoning":
        if model["source"] == "openai":
            system_prompt = get_system_prompt_for_openai_reasoning()
        elif model["source"] == "anthropic":
            system_prompt = get_system_prompt_for_anthropic_reasoning()
        elif model["source"] == "deepseek":
            system_prompt = get_system_prompt_for_deepseek_reasoning()
    else:
        system_prompt = create_chat_message("system", system_prompt_social)
    return system_prompt


def get_system_prompt_for_openai_reasoning():
    return create_chat_message("developer", system_prompt_social)


def get_system_prompt_for_anthropic_reasoning():
    return create_chat_message("assistant", system_prompt_social)


def get_system_prompt_for_deepseek_reasoning():
    return create_chat_message("assistant", system_prompt_social)
