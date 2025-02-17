import os
import sys
import dotenv
import pytest

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
print(project_root)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)

from engine.flow.handle_reply_flow.handle_reply_flow import handle_reply_flow
from engine.utils.json_util import extract_code_breakdown_from_doc, extract_str_from_doc

engine_output = """BTC is the abbreviation for Bitcoin, the world's first and most well-known cryptocurrency. Bitcoin is a decentralized digital currency that operates without a central authority or banks. It can be sent from user to user on the peer-to-peer bitcoin network and is secured through cryptography. Bitcoin was created in 2009 by an anonymous person or group using the name Satoshi Nakamoto."""

chat_messages = [
    {"role": "user", "content": "What is Bitcoin?"},
    {"role": "assistant", "content": engine_output},
]

final_reply = handle_reply_flow(chat_messages, [{"normal_llm_reply": engine_output}])

analysis = extract_code_breakdown_from_doc(final_reply)
final_reply = extract_str_from_doc(final_reply)

print(f"final_reply: {final_reply}")
