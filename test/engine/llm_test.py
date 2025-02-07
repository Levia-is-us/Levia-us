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

from engine.llm_provider.llm import chat_completion, create_chat_completion, create_embedding


# Test chat_completion  
# print(chat_completion([{"role": "user", "content": "Hello, how are you?"}]))

# Test create_chat_completion
# print(create_chat_completion("You are a helpful assistant", "Hello, how are you?"))

# Test create_embedding
result = create_embedding("Hello, how are you?")
print(result)
