from openai import OpenAI

import os

from engine.utils.chat_formatter import (
    convert_system_message_to_developer_message,
    pop_system_message_to_developer_message,
)
from metacognitive.stream.stream import output_stream

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"


def chat_completion_deepseek(messages, model, config={}):
    """
    Generate chat completion using OpenAI API.

    Parameters:
    - messages: List of messages to simulate a conversation
      Each message is a dictionary containing the role ("user" or "system" or "assistant") and content ("content").

    Returns:
    - model reply message content
    """
    try:
        client = OpenAI(base_url="", api_key=api_key)
        if model["type"] == "reasoning":
            messages = pop_system_message_to_developer_message(messages)
        completion_params = {
            "model": model["model"],
            "messages": messages,
            "max_tokens": 2000,
            "stream": False,
        }
        # Update with any additional config parameters
        completion_params.update(config)

        completion = client.chat.completions.create(**completion_params)

        if model["type"] == "reasoning":
            if completion.choices[0].message.model_extra:
                reasons = completion.choices[0].message.model_extra.reasoning_content
                output_stream(reasons)

        # Extract the model reply
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
