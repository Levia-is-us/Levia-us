from engine.llm_provider.llm import chat_completion
import os
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

def backup_reply(chat_messages, user_id="local-dev", ch_id=""):
    try:
        backup_llm_prompt = "You are Levia, an advanced AI agent within the Levia ecosystem with the unique ability to learn and grow over time."
        propmt = [
            {"role": "system", "content": backup_llm_prompt},
            {"role": "user", "content": chat_messages}
        ]
        result = chat_completion(propmt, CHAT_MODEL_NAME, config={"temperature": 0}, user_id=user_id, ch_id=ch_id)
        return result
    except Exception as e:
        print(f"Our system is currently experiencing high traffic. We kindly ask that you please try again later.")
        return None
