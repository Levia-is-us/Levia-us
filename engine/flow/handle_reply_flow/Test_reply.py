import sys
import os

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from engine.flow.handle_reply_flow.final_reply_prompt import final_reply_prompt
from engine.llm_provider.llm import chat_completion



def final_reply_flow(chat_messages: list, engine_output: list) -> str:
    """Handle final reply type response"""
    prompt = final_reply_prompt(chat_messages, engine_output)
    final_reply = chat_completion(
        prompt, model="deepseek-r1", config={"temperature": 0.7}
    )

    return final_reply


def main():
    #chat_messages = input("Enter your message: ")
    # result = get_initial_response([{"role": "user", "content": chat_messages}])
    chat_messages = [
        {"role": "user", "content": "Hello, how are you?"}
        ]
    engine_output = []
    result = final_reply_flow(chat_messages, engine_output)
    print(result)


if __name__ == "__main__":
    main()


