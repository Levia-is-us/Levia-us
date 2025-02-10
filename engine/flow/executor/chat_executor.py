from engine.llm_provider.llm import chat_completion
from memory.episodic_memory.episodic_memory import retrieve_short_pass_memory
from engine.flow.executor.tool_executor import execute_tool
from engine.flow.planner.planner import create_execution_plan, check_plan_sufficiency
from engine.utils.json_util import extract_json_from_str
import json

from engine.tool_framework.tool_caller import ToolCaller
from engine.flow.executor.tool_executor import verify_tool_execution
from engine.flow.tool_selector.tool_select import tool_select
from engine.flow.tool_selector.step_necessity_validator import step_tool_check
from engine.flow.executor.next_step_prompt import next_step_prompt
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")

def process_existing_memories(
    high_score_memories: list,
    summary: str,
    execution_records_str: list,
    messages_history: list,
    tool_caller: ToolCaller,
) -> str:
    """Process existing memories from database"""
    top_memory = high_score_memories[0]
    try:
        execution_records = [
            eval(record) for record in top_memory["metadata"]["execution_records"]
        ]
        if check_plan_sufficiency(summary, top_memory["id"], execution_records):
            res = execute_existing_records(execution_records, tool_caller)
            return str(res)
    except Exception as e:
        print(f"execute existing records error: {str(e)}")

    # create plan & tool execution context
    plan = create_execution_plan(summary)
    tool_result_records = handle_new_tool_execution(
        execution_records_str, summary, plan, tool_caller, messages_history
    )
    return str(tool_result_records)


def execute_existing_records(execution_records: list, tool_caller) -> dict:
    """Execute existing tool records"""
    for record in execution_records:
        try:
            if isinstance(record, str):
                record = extract_json_from_str(record)
            result, _ = execute_tool(
                tool_caller, record["tool"], record["method"], record["args"]
            )
            print(f"Executed tool: {record['tool']}.{record['method']}")
            print(f"Result: {result}")
            return result
        except Exception as e:
            print(f"Error processing execution record: {str(e)}")
            raise e



def handle_new_tool_execution(execution_records_str, summary, plan, tool_caller, messages_history: list) -> list:
    """
    Handle execution of new tools based on the plan
    
    Args:
        execution_records_str: List to store execution records
        summary: Summary of the execution plan
        plan: Plan containing steps to execute
        tool_caller: Tool caller instance to execute tools
        messages_history: History of conversation messages
        
    Returns:
        list: Records of tool execution results
    """
    plan_steps = eval(plan)
    tool_results = []
    
    # Analyze each step and find appropriate tools
    for step in plan_steps:
        print(f"Processing step: {step}")
        if not _process_plan_step(step, plan, messages_history, plan_steps):
            print(f"\033[91mFailed to process step: {step['Description']}\033[0m")
            return []
            
    # Execute tools for each plan step
    for step in plan_steps:
        if not step.get("tool_necessity", True):
            continue
            
        tool_result = _execute_plan_step(
            step, 
            tool_caller, 
            messages_history, 
            execution_records_str,
            plan_steps
        )
        if tool_result:
            tool_results.append(tool_result)
            
    return tool_results

def _process_plan_step(step, plan, messages_history, plan_steps):
    """
    Process a single plan step to determine tool necessity and find appropriate tool
    """
    # Check if step is necessary
    necessity_check = _check_step_necessity(step, plan, messages_history, plan_steps)
    if not necessity_check["steps_necessity"] == "Yes":
        step["tool_necessity"] = False
        return True
        
    # Find appropriate tool for the step
    return _find_tool_for_step(step, plan, messages_history)
    
def _check_step_necessity(step, plan, messages_history, plan_steps):
    """Check if a step is necessary to execute"""
    result = step_tool_check(plan, step, messages_history, plan_steps)
    return extract_json_from_str(result)

def _find_tool_for_step(step, plan, messages_history):
    """Find appropriate tool for a step from memory"""
    memories = retrieve_short_pass_memory(step["Description"])
    if not memories:
        return False
        
    tool_selection = tool_select(plan, step, messages_history, memories)
    tool_selection = extract_json_from_str(tool_selection)
    tool_name = tool_selection["tool_name"]
    
    # Search for tool in memories
    if "matches" in memories:
        for match in memories["matches"]:
            if match["id"] == tool_name:
                step["tool_necessity"] = True
                step["execution_tool"] = match
                return True
    return False

def _execute_plan_step(step, tool_caller, messages_history, execution_records, plan_steps):
    """
    Execute tool for a plan step
    
    Returns:
        str: Tool execution record if successful, None otherwise
    """
    tool = step["tool"]
    tool_config = _get_tool_config(tool)
    if not tool_config:
        return None
        
    while True:
        execution_result = _try_execute_tool(
            tool_config,
            tool_caller,
            messages_history,
            plan_steps,
            step
        )
        
        if execution_result:
            execution_records.append(tool)
            step["execution_tool_result"] = execution_result
            return f"toolName: {tool_config['tool']} result: {execution_result}"
            
        if not _handle_failed_execution(messages_history):
            return None

def _get_tool_config(tool):
    """Extract and parse tool configuration"""
    tool_dict = tool["metadata"]["data"]
    if isinstance(tool_dict, str):
        return extract_json_from_str(tool_dict)
    return tool_dict

def _try_execute_tool(tool_config, tool_caller, messages_history, plan_steps, step):
    """Attempt to execute tool with current configuration"""
    next_step_content = next_step_prompt(plan_steps, tool_config, messages_history)
    prompt = [{"role": "assistant", "content": next_step_content}]
    
    reply = chat_completion(prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0.5})
    reply_json = extract_json_from_str(reply)
    print(f"\033[92mAssistant: {reply_json}\033[0m")
    
    if reply_json["can_proceed"]:
        return _execute_tool_with_args(tool_config, tool_caller, reply_json)
    return None

def _execute_tool_with_args(tool_config, tool_caller, reply_json):
    """Execute tool with provided arguments"""
    args = reply_json["extracted_arguments"].get("required_arguments", {})
    result = execute_tool(
        tool_caller,
        f"{tool_config['method']}_tool",
        tool_config['method'],
        args
    )
    print(f"Tool execution result: {result}")
    
    if verify_tool_execution(tool_config, result) == "success":
        return result
    return None

def _handle_failed_execution(messages_history):
    """Handle failed tool execution by requesting user input"""
    user_input = input("Please input required arguments to continue: ")
    if not user_input:
        return False
    messages_history.append({"role": "user", "content": user_input})
    return True


def filter_high_score_memories(memories: dict, threshold: float = 0) -> list:
    """Filter and sort memories by score"""
    if not memories or "matches" not in memories:
        return []

    high_score_matches = [
        match for match in memories["matches"] if match.get("score", 0) >= threshold
    ]

    return sorted(high_score_matches, key=lambda x: x.get("score", 0), reverse=True)
