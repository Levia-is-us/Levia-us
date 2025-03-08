import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)

from engine.flow.handle_intent_flow.analyze_intent_flow import handle_intent_flow

def main():
    input_messages = "panda: Will BTC going up in the flowing days?"
    message = """Please help me answer this tweet: 
<tweet>
{input_messages}
</tweet>
If your result contains 'call_tool' operation, also save the knowledge into a document and upload it to **gitbook**.
<output_example>
{{
"result": "The president of the United States is Joe Biden.",
"call_tool": "User ask about the president of the United States and want to save the knowledge into a document and upload it to **gitbook**."
}}
</output_example>
    """
    input_message = message.format(input_messages=input_messages)
    # chat_messages = input("Enter your message: ")
    # chat_messages = [{"role": "user", "content": input_messages}]
    print(input_message)
    result = handle_intent_flow(chat_messages=[], input_message=input_message, user_id="local-dev")
    print(result)



if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
