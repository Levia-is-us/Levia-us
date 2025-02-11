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
        client = OpenAI(base_url=base_url, api_key=api_key)
        if model["type"] == "reasoning":
            messages = pop_system_message_to_developer_message(messages)
        completion_params = {
            "model": model["model"],
            "messages": messages,
            "max_tokens": 2000,
            "stream": True,
        }
        # Update with any additional config parameters
        completion_params.update(config)
        completion = client.chat.completions.create(**completion_params)
        
        full_response = ""
        buffer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                buffer += content
                
                if "<input_breakdown>" in buffer:
                    start = buffer.find("<input_breakdown>") + len("<input_breakdown>")
                    end = buffer.find("</input_breakdown>")
                    if end != -1:
                        breakdown = buffer[start:end]
                        # 按 " - " 分割并打印每一行
                        for line in breakdown.split("\n"):
                            if " - " in line:
                                parts = line.split(" - ")
                                for part in parts:
                                    if part.strip():
                                        output_stream(f" - {part.strip()} - \n")
                        buffer = buffer[end+len("</input_breakdown>"):]
                    else:
                        buffer = buffer[start:]
                elif " - " in buffer and model["type"] == "reasoning":
                    sentences = buffer.split(" - ")
                    for sentence in sentences[:-1]:
                        if sentence.strip():
                            output_stream(f" - {sentence.strip()} - \n")
                    buffer = sentences[-1]
        
        if "<input_breakdown>" in buffer:
            start = buffer.find("<input_breakdown>") + len("<input_breakdown>")
            end = buffer.find("</input_breakdown>")
            if end != -1:
                breakdown = buffer[start:end]
                for line in breakdown.split("\n"):
                    if " - " in line:
                        parts = line.split(" - ")
                        for part in parts:
                            if part.strip():
                                output_stream(f" - {part.strip()} - \n")
        elif buffer and model["type"] == "reasoning":
            output_stream(f" - {buffer.strip()} - \n")

        return full_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
