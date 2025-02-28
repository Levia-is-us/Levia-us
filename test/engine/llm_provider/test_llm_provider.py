import pytest
import os
import sys
import dotenv

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

from engine.llm_provider.llm import create_chat_completion


def test_llm_provider(model="gpt-4.5-preview"):
    response = create_chat_completion(
        system_prompt="You are a helpful assistant.",
        prompt="What is the capital of the moon?",
        model=model,
    )

    print(response)


if __name__ == "__main__":
    import time

    models = ["gpt-4.5-preview", "claude-3-7-sonnet-20250219", "deepseek-reasoner"]
    for model in models:
        start_time = time.time()
        test_llm_provider(model)
        end_time = time.time()
        print(f"Test {model}, execution time: {end_time - start_time:.2f} seconds")
