import re
from openai import OpenAI

import os

from engine.utils.chat_formatter import (
    convert_system_message_to_developer_message,
    pop_system_message_to_developer_message,
)
from metacognitive.stream.stream import output_stream

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"

def print_buffer_to_stream(buffer, user_id, buffer_type, ch_id):
    buffer = format_content(buffer)
    if not buffer or buffer == "":
        return
    # if buffer_type == "think":
    #     print("\033[32m" + buffer + "\033[0m")
    # elif buffer_type == "input_breakdown":
    #     print("\033[31m" + buffer + "\033[0m")
    # else:
    #     print("\033[32m" + buffer + "\033[0m")
    output_stream(log=f"{buffer}", user_id=user_id, type='think', ch_id=ch_id)
def format_content(content):
    if not content or content == "":
        return ""
    content = content.replace("\n", "")
    content = content.replace("-", "")
    return content

def chat_completion_deepseek(messages, model, config={}, user_id="", ch_id=""):
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
            "max_tokens": 4000,
            "stream": True,
        }
        # Update with any additional config parameters
        completion_params.update(config)
        completion = client.chat.completions.create(**completion_params)

        if not completion_params.get("stream", False):
            return completion.choices[0].message.content
        # <think>
        
        full_response = ""
        buffer = ""
        buffer_type = ""
        print_stream = False
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if not content or content == "":
                continue
            full_response += content
            buffer_end = re.search("</([^>]+)|</()", content)
            buffer_start = re.search("<([^>]+)", content)
            buffer_new_line = re.search("\n", content) or re.search("- ", content)
            content = format_content(content)
            
            if buffer_new_line:
                if print_stream:
                    print_buffer_to_stream(buffer, user_id, buffer_type, ch_id)
                buffer = ""
                continue

            if buffer_end:
                # output 
                if print_stream:
                    print_buffer_to_stream(buffer, user_id, buffer_type, ch_id)
                buffer_type = ""
                buffer = ""
                print_stream = False
                continue
                
            if buffer_start:
                buffer_type = buffer_start.group(1)
                buffer = ""
                print_stream = True
                continue
            
            buffer += content

        return full_response
    except Exception as e:
        print("\033[31m" + f"An error occurred: {e}" + "\033[0m")
        return None

# <think>
# </think>

# <input_breakdown>
# </input_breakdown>

# ```json
# ```
