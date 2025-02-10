import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.executor.check_tools_result_prompt import check_tools_result_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str


""" This LLM is used to verify the tool is executed successfully or not"""

def verify_tool_execution(execution_record: dict, result: dict) -> str:
    """Verify tool execution result using LLM"""
    llm_check_prompt = check_tools_result_prompt(
        tool_execution=str(execution_record),
        tool_output=result
    )
    
    llm_confirmation = chat_completion(
        llm_check_prompt,
        model="deepseek-chat",
        config={"temperature": 0.7}
    )
    
    llm_confirmation = extract_json_from_str(llm_confirmation)
    #todo: add error handling
    return llm_confirmation

if __name__ == "__main__":
    """put your tool execution record and result here
        for format reference like:
        execution_record = {
                            "tool": "tool_name", 
                            "method": "method_name",
                            "description": "description", 
                            "input": {"arg1": "value1", "arg2": "value2"},
                            "output": "result_output"
                            }
        result = {"output": "result_output"}
    """
    execution_record = "execution_record"
    result = "result"
    print(verify_tool_execution(execution_record, result))