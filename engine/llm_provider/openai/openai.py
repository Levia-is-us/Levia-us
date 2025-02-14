from openai import AzureOpenAI, OpenAI
import os

from engine.utils.chat_formatter import (
    convert_system_message_to_developer_message,
    pop_system_message_to_developer_message,
)
from engine.utils.tokenizer import is_message_too_long
from metacognitive.stream.stream import output_stream

api_key = os.getenv("OPENAI_API_KEY")
host = os.getenv("OPENAI_BASE_URL")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_host = os.getenv("AZURE_OPENAI_BASE_URL")


def chat_completion_openai(
    messages,
    model={
        "model": "gpt-35-turbo-16k",
        "version": "2024-05-01-preview",
        "type": "chat",
        "source": "azure-openai",
    },
    config={},
):
    """
    Generate chat completion using OpenAI API.

    Parameters:
    - messages: List of messages to simulate a conversation
      Each message is a dictionary containing the role ("user" or "system" or "assistant") and content ("content").

    Returns:
    - model reply message content
    """
    try:
        # check request is too long
        if model["context_window_size"] and is_message_too_long(
            messages, model["context_window_size"], config.get("max_tokens", 800)
        ):
            raise Exception(
                f"LLM model request message is too long, model: {model['model']}, context_window_size: {model['context_window_size']}, max_tokens: {config.get('max_tokens', 800)}"
            )

        client = None
        if model["source"] == "azure-openai":
            client = AzureOpenAI(
                azure_endpoint=azure_host,
                api_key=azure_api_key,
                api_version=model["version"],
            )
        else:
            client = OpenAI(api_key=api_key, base_url=host)
        # Remove default parameters that might conflict with config

        if model["type"] == "reasoning":
            # messages = convert_system_message_to_developer_message(messages)
            messages = pop_system_message_to_developer_message(messages)

        completion_params = {
            "model": model["model"],
            "messages": messages,
            "max_tokens": 800,
            "stream": False,
        }
        # Update with any additional config parameters
        completion_params.update(config)

        if model["type"] == "reasoning":
            completion_params = {
                "model": model["model"],
                "messages": messages,
                "max_completion_tokens": completion_params["max_tokens"],
                "stream": False,
            }

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


def generate_embeddings(text, model="text-embedding", version="2023-05-15"):
    client = AzureOpenAI(
        api_key=azure_api_key,
        api_version=version,
        azure_endpoint=azure_host,
        max_retries=0,
    )
    data = client.embeddings.create(input=[text], model=model)
    return data.data[0].embedding
