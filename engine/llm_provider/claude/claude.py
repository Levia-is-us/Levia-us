import anthropic
import os

api_key = os.getenv("ANTHROPIC_API_KEY")


def chat_completion_anthropic(messages, model="claude-3-5-sonnet-20241022", config={}):
    """
    Generate chat completion using Anthropic API.

    Parameters:
    - messages: List of messages to simulate a conversation
      Each message is a dictionary containing the role ("user" or "system" or "assistant") and content ("content").
    - version: Model version to use (default: claude-3-5-sonnet-20241022)
    - config: Additional configuration parameters to pass to the API

    Returns:
    - model reply message content
    """
    client = anthropic.Anthropic(
        api_key=api_key,
    )
    default_config = {
        "max_tokens": 4000
    }
    config.update(default_config)

    message = client.messages.create(model=model, messages=messages, **default_config)
    return message.content[0].text
