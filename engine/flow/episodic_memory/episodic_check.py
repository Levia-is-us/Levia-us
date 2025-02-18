from engine.flow.episodic_memory.episodic_check_prompt import episodic_check_prompt
from engine.llm_provider.llm import chat_completion
import os
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def episodic_check(user_intent, context, plan):
    prompt = episodic_check_prompt(user_intent, context, plan)
    result = chat_completion(prompt, model_name=QUALITY_MODEL_NAME, config={"temperature": 0})
    return result

