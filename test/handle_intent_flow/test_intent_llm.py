import sys
import os

# Get absolute path of current file

current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from engine.flow.handle_intent_flow.handle_intent_flow import handle_intent_flow
from engine.utils.json_util import extract_json_from_str

def main():
    input_messages = "What is the latest news about OpenAI?"
    # chat_messages = input("Enter your message: ")
    # chat_messages = [{"role": "user", "content": input_messages}]

    result = handle_intent_flow(chat_messages=[], input_message=input_messages)
    print(result)




if __name__ == "__main__":
    main()
