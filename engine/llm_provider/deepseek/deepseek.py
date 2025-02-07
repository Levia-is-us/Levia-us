from openai import OpenAI

import os

api_key = os.getenv("DEEPSEEK_API_KEY")

def chat_completion_deepseek(messages, model="deepseek-chat", config={}):
    """
    Generate chat completion using OpenAI API.

    Parameters:
    - messages: List of messages to simulate a conversation
      Each message is a dictionary containing the role ("user" or "system" or "assistant") and content ("content").

    Returns:
    - model reply message content
    """
    try:
        client = OpenAI(base_url="https://api.deepseek.com", api_key=api_key)
        completion_params = {
            "model": model,
            "messages": messages,
            "max_tokens": 2000,
            "stream": False,
        }
        # Update with any additional config parameters
        completion_params.update(config)

        completion = client.chat.completions.create(**completion_params)

        # Extract the model reply
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
