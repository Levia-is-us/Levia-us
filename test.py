from openai import OpenAI

base_url = "http://45.126.210.175:3009/v1/"
api_key = "sk-KEVSWmIsJBSSqULNohzyteJxDGepUCl0cZJHJ8cmESqO9DYA"

client = OpenAI(base_url=base_url, api_key=api_key)
completion_params = {
    "model": "deepseek-reasoner",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "max_tokens": 2000,
    "stream": False,
}
# Update with any additional config parameters
completion = client.chat.completions.create(**completion_params)

print(completion)