import sys
import os

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (2 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from engine.flow.handle_intent_flow.handle_intent_flow import handle_intent_flow
from engine.utils.json_util import extract_json_from_str

def main():
    input_messages = "panda: who is the president of the United States?"
    message = """I will provide you a twitter user name with the user's request from Twitter, and I hope you can fulfill the user's request. if the query requires the execution of a 'call_tool' operation, add one more intent: the knowledge into a document and upload it to Levia's **gitbook**.
 to Levia's **gitbook**.
 Twitter requirement: {input_messages}
    """
    input_message = message.format(input_messages=input_messages)
    # chat_messages = input("Enter your message: ")
    # chat_messages = [{"role": "user", "content": input_messages}]
    print(input_message)
    result = handle_intent_flow(chat_messages=[], input_message=input_message, user_id="local-dev")
    print(result)




if __name__ == "__main__":
    main()
