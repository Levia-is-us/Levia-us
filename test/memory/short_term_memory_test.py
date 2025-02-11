import os
import sys
import dotenv

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from memory.short_term_memory.short_term_memory import ShortTermMemory

short_term_memory = ShortTermMemory(max_length=60)

# 50 tokens
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hello! Happy to help you."},
    {"role": "user", "content": "What is 1+1?"},
    {"role": "assistant", "content": "1+1=2"},
]

short_term_memory.add_context(messages)

print(short_term_memory.get_context())

# add 6 tokens
short_term_memory.add_context({"role": "assistant", "content": "Hello1"})
short_term_memory.add_context({"role": "user", "content": "Hello2"})
short_term_memory.add_context({"role": "assistant", "content": "Hello3"})

# should see the content "You are a helpful assistant" removed
print(short_term_memory.get_context())


