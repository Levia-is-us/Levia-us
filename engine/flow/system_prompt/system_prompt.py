from engine.utils.chat_formatter import create_chat_message


system_prompt = """Your name is Levia, and you are an AI strategist in a Living Agent Ecosystem, help user to do running tasks and answer questions."""
# You should blend technical precision with accessible language, blend technical precision with accessible language, lead with bold insights, support with layered analysis, connect specific observations to broader trends, use tech/startup metaphors and concrete examples"""


def get_system_prompt():
    return create_chat_message("system", system_prompt)


def get_system_prompt_for_openai_reasoning():
    return create_chat_message("developer", system_prompt)


def get_system_prompt_for_anthropic_reasoning():
    return create_chat_message("user", system_prompt)


def get_system_prompt_for_deepseek_reasoning():
    return create_chat_message("assistant", system_prompt)
