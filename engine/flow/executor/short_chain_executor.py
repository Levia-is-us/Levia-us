from engine.llm_provider.llm import chat_completion
from memory.episodic_memory.episodic_memory import retrieve_short_pass_memory
from engine.flow.executor.tool_executor import execute_tool
from engine.flow.planner.planner import create_execution_plan
from engine.utils.json_util import extract_json_from_str
import json

from engine.tool_framework.tool_caller import ToolCaller
from engine.flow.executor.tool_executor import verify_tool_execution
from engine.flow.tool_selector.tool_select import tool_select
from engine.flow.tool_selector.step_necessity_validator import step_tool_check
from engine.flow.executor.next_step_prompt import next_step_prompt
import os
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.utils.chat_formatter import create_chat_message
from engine.tool_framework.tool_caller import ToolCaller
from engine.tool_framework.tool_registry import ToolRegistry
from memory.plan_memory.plan_memory import PlanContextMemory
from metacognitive.stream.stream import output_stream

registry = ToolRegistry()
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
print(f"registry project_root: {project_root}")
tools_dir = os.path.join(project_root, "tools")
registry.scan_directory(tools_dir)
tool_caller_client = ToolCaller(registry)

plan_context_memory = PlanContextMemory()
short_term_memory = ShortTermMemory()
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")
INTERACTION_MODE = os.environ["INTERACTION_MODE"]

def short_chain_executor(
    user_intent: str,
    messages_history: list,
    user_id: str
):   
    output_stream(f" - Do not have experience for {user_intent} - \n")
    output_stream(f" - Creating new execution plan ... - \n")
    plan = create_execution_plan(user_intent)
    handle_new_tool_execution(
        plan, messages_history, user_id
    )
    return plan

def handle_new_tool_execution(plan, messages_history: list, user_id: str):
    """
    Handle execution of new tools based on the plan
    
    Args:
        execution_records_str: List to store execution records
        summary: Summary of the execution plan
        plan: Plan containing steps to execute
        messages_history: History of conversation messages
        
    Returns:
        list: Records of tool execution results
    """
    
    # Analyze each step and find appropriate tools
    for step_index, step in enumerate(plan):
        print(f"\033[93mFinding appropriate tool for step: {step['intent']} - \033[0m\n")
        found_tools.extend(resolve_tool_for_step(step))

    #replan
    found_tools = get_unique_tools(found_tools)
    print(f"\033[93mMaking new plan based on current tools - \033[0m\n")
    plan = tool_base_planner(user_intent, found_tools)
    print(f"plan: {plan}")
            
    if(plan["status"] == "Failed to make plan with current tools"):
        print(f"\033[93m - Failed to make plan with current tools - \033[0m\n")
        return plan
    plan = plan["plan"]

    # Execute tools for each plan step
    execute_plan_steps(messages_history, plan, user_id)
    
    all_steps_executed = all(step.get("executed", False) for step in plan)
    if all_steps_executed:
        plan_context_memory.create_plan_context(plan, user_id)

def _get_tools_from_plan_steps(plan_steps):
    tools = []
    for step in plan_steps:
        if 'tool' in step and step['tool'] not in tools:
            tools.append(step['tool'])
    return tools

def execute_plan_steps(messages_history, plan_steps, user_id: str):
    # tool_results = []
    for step_index, step in enumerate(plan_steps):
        if not step.get("tool_necessity", True):
            continue
        if step.get("executed", False):
            continue
            
        tool_result = _execute_plan_step_tool(
            messages_history,
            step,
            plan_steps,
            user_id,
            step_index
        )
        step["tool_executed_result"] = tool_result["result"]
        if tool_result["status"] == "failure":
            step["executed"] = True
            break
        elif tool_result["status"] == "need_input":
            step["executed"] = False
            break
        else:
            step["executed"] = True
    # return tool_results

def _process_plan_step(step, plan, messages_history, step_index, user_id: str, found_tools):
    """
    Process a single plan step to determine tool necessity and find appropriate tool
    """
    if found_tools is None:
        found_tools = []
    # Check if step is necessary
    necessity_check = _check_step_necessity(step, plan, messages_history, found_tools)
    if not necessity_check["steps_necessity"] == "Yes":
        step["tool_necessity"] = False
        # plan_context_memory.update_step_status_context(step_index, tool_necessity=False, user_key=user_id)
        return True
        
    # Find appropriate tool for the step
    return _find_tool_for_step(step, plan, messages_history, step_index, user_id)
    
def _check_step_necessity(step, plan, messages_history, done_steps):
    """Check if a step is necessary to execute"""
    result = step_tool_check(plan, step, messages_history, done_steps)
    return extract_json_from_str(result)

def _find_tool_for_step(step, plan, messages_history, step_index, user_id: str):
    """Find appropriate tool for a step from memory"""
    memories = retrieve_short_pass_memory(step["Description"])
    if not memories:
        return False
    
    # print(f"Finding tool for step: {memories}")
    tool_name = tool_select(plan, step, messages_history, memories)
    # Search for tool in memories
    if "matches" in memories:
        for match in memories["matches"]:
            if match["metadata"]["tool"] == tool_name:
                del match["metadata"]["description"]
                step["tool"] = match
                step["tool_necessity"] = True
                # plan_context_memory.update_step_status_context(step_index, tool_necessity=True, execution_tool=match, user_key=user_id)
                return True
    step["tool"] = "No tool found for current step"
    step["tool_necessity"] = True
    return False

def _execute_plan_step_tool(messages_history,step, plan_steps, user_id: str, step_index: int):
    """
    Execute tool for a plan step
    
    Returns:
        str: Tool execution record if successful, None otherwise
    """
    tool = step["tool"]
    tool_config = _get_tool_config(tool)
    if not tool_config:
        return None
    
    tool_name = tool_config['tool']
    
    def execute_with_config(messages_history):
        reply_json = _check_required_extra_params(
            tool_config,
            messages_history, 
            plan_steps,
            step
        )
        
        if not reply_json["can_proceed"]:
            return {
                "toolName": tool_name,
                "result": f"Please input required arguments to continue: {reply_json['missing_required_arguments']}", 
                "status": "need_input"
            }
            
        execution_result = _execute_tool_with_args(tool_config, reply_json)
        if execution_result["status"] == "failure":
            return {
                "toolName": tool_name,
                "result": "execution failed",
                "status": "failure"
            }
            
        if execution_result:
            plan_context_memory.update_step_status_context(
                step_index,
                execution_result=execution_result,
                executed=True,
                user_key=user_id
            )
            return {
                "toolName": tool_name,
                "result": execution_result,
                "status": "success"
            }
            
        return None
    
    if INTERACTION_MODE == "terminal":
        while True:
            result = execute_with_config(messages_history)
            if result and result["status"] == "success":
                return result
            elif result and result["status"] == "need_input":
                if not _handle_terminal_input(user_id):
                    return None
                messages_history.append(short_term_memory.get_context(user_id))
            else:
                return result
    else:
        return execute_with_config(messages_history)

def _get_tool_config(tool):
    """Extract and parse tool configuration"""
    tool_dict = tool["metadata"]["data"]
    tool_name =tool["metadata"]["tool"]
    if isinstance(tool_dict, str):
        tool_dict = extract_json_from_str(tool_dict)
    tool_dict["tool"] = tool_name
    return tool_dict

def _check_required_extra_params(tool_config, messages_history, plan_steps, step):
    """Attempt to execute tool with current configuration"""
    next_step_content = next_step_prompt(plan_steps, tool_config, messages_history)
    prompt = [{"role": "user", "content": next_step_content}]
    
    reply = chat_completion(prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0.5})
    reply_json = extract_json_from_str(reply)
    output_stream(f" - {reply_json} - \n")
    return reply_json

def _execute_tool_with_args(tool_config, reply_json):
    """Execute tool with provided arguments"""
    args = reply_json["extracted_arguments"].get("required_arguments", {})
    result,_ = execute_tool(
        tool_caller_client,
        tool_config['tool'],
        tool_config['method'],
        args
    )
    print(f"Tool execution result: {result}")
    
    if verify_tool_execution(tool_config, result) == "success":
        return result
    return {"status": "failure"}

def _handle_terminal_input(user_id: str):
    """Handle failed tool execution by requesting user input"""
    user_input = input("Please input required arguments to continue: ")
    if not user_input:
        return False
    short_term_memory.add_context(create_chat_message("user", user_input), user_id)
    return True

def filter_high_score_memories(memories: dict, threshold: float = 0) -> list:
    """Filter and sort memories by score"""
    if not memories or "matches" not in memories:
        return []

    high_score_matches = [
        match for match in memories["matches"] if match.get("score", 0) >= threshold
    ]

    return sorted(high_score_matches, key=lambda x: x.get("score", 0), reverse=True)