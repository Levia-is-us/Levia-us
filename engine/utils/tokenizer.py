import tiktoken

def num_tokens_from_string(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Calculate the number of tokens in a string
    
    Args:
        string: The string to calculate tokens for
        model_name: Model name, defaults to gpt-3.5-turbo
        
    Returns:
        Number of tokens
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def num_tokens_from_messages(messages: list, model_name: str = "gpt-3.5-turbo") -> int:
    """Calculate the number of tokens in a message list
    
    Args:
        messages: List of messages, each message in dict format
        model_name: Model name, defaults to gpt-3.5-turbo
        
    Returns:
        Number of tokens
    """
    encoding = tiktoken.encoding_for_model(model_name)
    
    # Base tokens per message
    tokens_per_message = 3
    # Base tokens per name
    tokens_per_name = 1
    
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":
                num_tokens += tokens_per_name
    # Base tokens per conversation        
    num_tokens += 3
    return num_tokens

