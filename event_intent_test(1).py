import os
from datetime import datetime
from pathlib import Path
import traceback
from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow
from engine.llm_provider.llm import chat_completion
import sys

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def extract_content_after_separator(text, separator="--------------------"):
    """
    Extract the content after a separator
    """
    if separator in text:
        return text.split(separator, 1)[1].strip()
    return text


def event_chat(input_message, user_id="local-dev"):
    reply = handle_chat_flow(input_message, user_id, chid = "")
    text = extract_content_after_separator(reply)
    print(f"=============== Levia Reply: {text}")
    return text


def generate_chat_msg(reply: str) -> str:
    """
    Generate a chat message from the reply

    Args:
        reply (str): The reply from the chatbot

    Returns:
        str: The chat message
    """
    prompt = """
    You are a sharp QA tester for an AI product named Levia. Below is the introduction of Levia:
    "I am Levia, an AI strategist in the Living Agent Ecosystem. I can assist you with a variety of tasks including analyzing information, answering questions, problem-solving, and providing recommendations based on context. My goal is to aid you through conversation and strategic thinking, although I am unable to perform physical actions or access external systems."

    Your task is to keep communicating with Levia continuously so as to check for potential bugs, and employ various testing methods to test for possible bugs in the Levia link.

    Requirements:
    - Ask questions that require internet search as possible.
    - The output should be only the response, no other text.

    Input:<Levia's reply>  
    Output: <Your response>

    Example Interaction:

    Input:  
    Levia: Hello! How can I assist you today?
    Output:  
    You: Hi Levia, can you help me analyze this data set?

    Input:  
    Levia: Sure, please provide the data set or describe its contents.
    Output:  
    You: It's a list of sales figures for the past quarter. Can you tell me the highest and lowest sales?
    """
    try:
        output = chat_completion(
            [
                {"role": "assistant", "content": prompt},
                {
                    "role": "user",
                    "content": f"Reply: {reply}",
                },
            ],
            model=CHAT_MODEL_NAME,
            config={"temperature": 1},
        )
        print(f"=============== User Reply: {output}")
        return output
    except Exception as e:
        return str(e)


class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            if hasattr(f, "closed") and f.closed:
                continue
            f.flush()


def main():
    # Add conversation log file path
    now_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = Path(__file__).parent / f"conversation_log_{now_time}.txt"
    try:
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            # Redirect stdout to Tee to log to file and console
            original_stdout = sys.stdout
            sys.stdout = Tee(original_stdout, log_file)
            print("========== Conversation Start ==========")
            levia_reply = "Welcome to Levia Chat!"
            print(f"Levia: {levia_reply}")
            while True:
                user_reply = generate_chat_msg(levia_reply)
                print(f"User: {user_reply}")
                levia_reply = event_chat(user_reply)
                print(f"Levia: {levia_reply}")
    except Exception as err:
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write("Program error:\n")
            log_file.write(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
