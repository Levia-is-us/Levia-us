import os
import sys
import time

# Get the absolute path of the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the project root (2 levels up from current file)
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Add the project root to Python's path
sys.path.insert(0, project_root)

from engine.llm_provider.llm import create_chat_completion

# Models to test
models = [
    "claude-3-5-sonnet",
    "claude-3-7-sonnet-20250219",
    "deepseek-v3",
    "deepseek-r1",
    "gpt-4o-mini",
]


def test_llm_provider():
    for model in models:
        start_time = time.time()
        output = create_chat_completion(
            system_prompt="You are a helpful assistant.",
            prompt="What is the capital of the moon?",
            model=model,
        )
        end_time = time.time()
        print("-" * 100)
        print(f"🤖  Model: {model}")
        print(f"📊  Output: {output}")
        print(f"⏱️  Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    test_llm_provider()
