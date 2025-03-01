import json
import os
from engine.llm_provider.llm import chat_completion
from dotenv import load_dotenv
import re

project_root = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

def get_markdown_title(text):
    prompt = f"""
        As a professional news editor, please create a title from the following content. Requirements:

        1. Keep it clear and concise (maximum 5 words)
        2. Use only simple English words (a-z, A-Z)
        3. No special characters, numbers, or symbols allowed
        4. Words should be meaningful and SEO-friendly
        5. The title must be URL-safe (only use letters)

        For example:
        Bad titles (don't use):
        - "AI & Machine Learning 2024!"
        - "Web3.0: Future's Here"
        - "Crypto @ Record High"

        Good titles (use these formats):
        - "Artificial Intelligence Transforms Healthcare"
        - "Bitcoin Reaches Market Peak"
        - "Global Climate Summit Results"

        Article content:
        {text}

        Please provide a title that best captures the essence of this article while following the above requirements.
        Only respond with the title, no explanations needed.
        """

    try:
        result = chat_completion(
            [
                {"role": "user", "content": prompt},
            ],
            model=CHAT_MODEL_NAME,
            config={"temperature": 0, "max_tokens": 2000, "stream": False},
        )


    except Exception as e:
        raise Exception(e)
    return format_text_for_url(result)



def replace_space_with_dash(text):
    return text.replace(' ', '-')


def format_text_for_url(text):
    text = text.strip()
    text = text.strip('"')
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = ' '.join(text.split())
    text = text.lower()
    return text
