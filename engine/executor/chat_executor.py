# engine/planner/planner.py

from engine.prompt_provider import (
    system_message,
    system_messagev2
)
from engine.llm_provider.llm import chat_completion
from memory.episodic_memory.episodic_memory import retrieve_short_pass_memory
from engine.executor.tool_executor import execute_tool
from engine.planner.planner import create_execution_plan, check_plan_sufficiency
from engine.flow.evaluator.evaluator_docgen_flow import extract_json_from_doc
import json
from engine.tool_framework.tool_caller import ToolCaller
from engine.executor.tool_executor import verify_tool_execution
from engine.executor.next_step_prompt import next_step_prompt

def process_existing_memories(high_score_memories: list, summary: str, execution_records_str: list, messages_history: list, tool_caller: ToolCaller) -> str:
    """Process existing memories from database"""
    top_memory = high_score_memories[0]
    execution_records = [eval(record) for record in top_memory["metadata"]["execution_records"]]
    
    try:
        if check_plan_sufficiency(summary, top_memory["id"], execution_records):
            res = execute_existing_records(execution_records, tool_caller)
            return str(res)
    except Exception as e:
        print(f"execute existing records error: {str(e)}")
    
    plan = create_execution_plan(summary)
    tool_result_records = handle_new_tool_execution(execution_records_str, summary, plan, tool_caller, messages_history)
    return str(tool_result_records)

def execute_existing_records(execution_records: list, tool_caller) -> dict:
    """Execute existing tool records"""
    for record in execution_records:
        try:
            if isinstance(record, str):
                record = extract_json_from_doc(record)
            result, _ = execute_tool(tool_caller, record["tool"], record["method"], record["args"])
            print(f"Executed tool: {record['tool']}.{record['method']}")
            print(f"Result: {result}")
            return result
        except Exception as e:
            print(f"Error processing execution record: {str(e)}")
            raise e

def process_new_intent(summary: str, execution_records_str: list, messages_history: list, tool_caller) -> None:
    """Process new intent without existing memories"""
    memories = retrieve_short_pass_memory(summary)
    messages_history.append({"role": "assistant", "content": system_message})
    reply = chat_completion(messages_history, model="deepseek-chat", config={"temperature": 0.3})
    print(f"\033[92mAssistant: {reply}\033[0m")
    
    try:
        tool_response = json.loads(reply)
        if isinstance(tool_response, dict):
            tool_name = tool_response.get("tool")
            tool_method = tool_response.get("method")
            tool_args = tool_response.get("arguments", {})
            
            if tool_name and tool_method:
                tool_record = {'tool': tool_name, 'method': tool_method, 'args': tool_args}
                result, execution_record = execute_tool(tool_caller, tool_name, tool_method, tool_args)
                execution_records_str.append(execution_record)
    except Exception as e:
        print(f"\033[91mError processing tool response: {str(e)}\033[0m")

def handle_new_tool_execution(execution_records_str, summary, plan, tool_caller, messages_history: list) -> list:
        """Handle execution of new tools"""
        plan_steps = eval(plan)
        tools = []
        tool_result_records = []
        # if len(plan_steps) > 1:
        for step in plan_steps:
            print(f"step: {step}")
            findTool = False
            # Check if step is already completed in tools collection. If not, get tool from short pass memory
            memories = retrieve_short_pass_memory(step["Description"])
            # Use LLM to extract appropriate tool from memories. Exit if no tool found
               
        if not findTool:
            print(f"\033[91mNo tool found for step: {step['Description']}\033[0m")
            return
        
        for tool in tools:
            tool_dict = extract_json_from_doc(tool)
            print(f"tool_dict: {tool_dict}")
            while True:
                next_step_prompt_content = next_step_prompt(tools, tool_dict)
                prompt = [{"role": "assistant", "content": next_step_prompt_content}] + messages_history
                reply = chat_completion(prompt, model="deepseek-chat", config={"temperature": 0.5})

                replyJson = extract_json_from_doc(reply)
                print(f"\033[92mAssistant: {replyJson}\033[0m")
                if(replyJson["can_proceed"] == True):
                    if "arguments" in replyJson["extracted_arguments"]:
                        required_arguments = replyJson["extracted_arguments"]["arguments"]
                    else:
                        required_arguments = {}
                    res = execute_tool(tool_caller, tool_dict["tool"], tool_dict["method"], required_arguments)
                    verify_res = verify_tool_execution(tool_dict, res)
                    if(verify_res == "success"):
                        execution_records_str.append(tool)
                        messages_history.append({"role": "assistant", "content":  tool_dict["tool"] + " result: " + str(res)})
                        tool_result_records.append("toolName: " + tool_dict["tool"] + " result: " + str(res))
                        print(f"\033[92mResult: {res}\033[0m")
                        break
                else:
                    inputText = input("Please input required arguments to continue: ")
                    messages_history.append({"role": "user", "content": inputText})
        return tool_result_records

def filter_high_score_memories(memories: dict, threshold: float = 0) -> list:
    """Filter and sort memories by score"""
    if not memories or 'matches' not in memories:
        return []
    
    high_score_matches = [
        match for match in memories['matches']
        if match.get('score', 0) >= threshold
    ]
    
    return sorted(
        high_score_matches,
        key=lambda x: x.get('score', 0),
        reverse=True
    )