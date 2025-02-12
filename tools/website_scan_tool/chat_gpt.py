from openai import AzureOpenAI
import os
from dotenv import load_dotenv

project_root = os.path.dirname(
    os.path.abspath(__file__)
)
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)


def chat_gpt(messages, config={}):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    client = AzureOpenAI(
        api_key=api_key, azure_endpoint=base_url, api_version="2024-05-01-preview"
    )

    completion_params = {
        "model": "gpt-35-turbo-16k",
        "messages": messages,
        "max_tokens": 2000,
        "stream": False,
    }
    completion_params.update(config)

    completion = client.chat.completions.create(**completion_params)

    # Extract the model reply
    return completion.choices[0].message.content
