import os
from engine.flow.mcp_adaption_flow.mcp_adaption_prompt import mcp_adaption_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str


def mcp_adaption_flow(tool_json_profile, server_id, source="smithery"):
    QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
    CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

    prompt = mcp_adaption_prompt(tool_json_profile, server_id)
    result = chat_completion(prompt, model=QUALITY_MODEL_NAME)

    extract_json = extract_json_from_str(result)

    extract_json["server_id"] = server_id
    extract_json["tool_name"] = tool_json_profile.get("name", "")
    extract_json["source"] = source
    return extract_json
