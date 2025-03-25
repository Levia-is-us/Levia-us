import os
import sys
import dotenv
import websockets

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from engine.utils.tokenizer import num_tokens_from_string, num_tokens_from_messages

# Example 1: Calculate tokens for single strings
test_strings = ["Hello World!", "Hello, World!", "Hello Hello World World!"]

models = ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"]

print("=== String Token Calculation ===")
for string in test_strings:
    print(f"\nText: {string}")
    for model in models:
        tokens = num_tokens_from_string(string, model)
        print(f"{model}: {tokens} tokens")

# Example 2: Calculate tokens for conversation messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hello! Happy to help you."},
    {"role": "user", "content": "What is 1+1?"},
    {"role": "assistant", "content": "1+1=2"},
]

print("\n=== Conversation Message Token Calculation ===")
for model in ["gpt-3.5-turbo", "gpt-4"]:
    tokens = num_tokens_from_messages(messages, model)
    print(f"{model}: {tokens} tokens")
