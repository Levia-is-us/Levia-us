def create_chat_message(role, content):
    return {"role": role, "content": content}


def create_chat_messages(messages):
    return [
        create_chat_message(message["role"], message["content"]) for message in messages
    ]


def remove_system_message(messages):
    return [
        message
        for message in messages
        if message["role"] != "assistant" and message["role"] != "system"
    ]


def pop_system_message_to_developer_message(messages):
    if (
        messages
        and len(messages) > 0
        and (messages[0]["role"] == "system" or messages[0]["role"] == "assistant")
    ):
        # remove first message
        messages.pop(0)

    return messages


def convert_system_message_to_developer_message(messages):
    if (
        messages
        and len(messages) > 0
        and (messages[0]["role"] == "system" or messages[0]["role"] == "assistant")
    ):
        # remove first message
        messages[0]["role"] = "developer"

    return messages
