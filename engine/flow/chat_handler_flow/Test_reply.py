import sys
import os

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from final_reply_prompt import final_reply_prompt
from engine.llm_provider.llm import chat_completion






def get_initial_response(chat_messages: list) -> dict:
    """Get initial response from LLM"""
    prompt = final_reply_prompt(chat_messages)
    reply_info = chat_completion(prompt, model="chatgpt-4o-latest", config={"temperature": 0.7})
    return reply_info


def main():
    #chat_messages = input("Enter your message: ")
    # result = get_initial_response([{"role": "user", "content": chat_messages}])
    chat_messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "{'type': 'direct_answer', 'response': 'Hello! How can I assist you today?'}"}
        ]
    result = get_initial_response(chat_messages)
    print(result)





if __name__ == "__main__":
    main()


