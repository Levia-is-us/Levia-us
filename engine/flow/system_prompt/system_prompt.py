from engine.utils.chat_formatter import create_chat_message


system_prompt = """Your name is Levia, and you are an AI strategist in a Living Agent Ecosystem, help user to do running tasks and answer questions."""


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
        system_prompt = create_chat_message("system", system_prompt)
    return system_prompt


def get_system_prompt_for_openai_reasoning():
    return create_chat_message("developer", system_prompt)


def get_system_prompt_for_anthropic_reasoning():
    return create_chat_message("assistant", system_prompt)


def get_system_prompt_for_deepseek_reasoning():
    return create_chat_message("assistant", system_prompt)
