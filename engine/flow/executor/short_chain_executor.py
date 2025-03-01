from engine.llm_provider.llm import chat_completion
from memory.episodic_memory.episodic_memory import retrieve_short_pass_memory
from engine.flow.executor.tool_executor import execute_tool
from engine.flow.planner.planner import create_execution_plan
from engine.utils.json_util import extract_json_from_str
from engine.tool_framework.tool_caller import ToolCaller
from engine.flow.tool_selector.step_necessity_validator import step_tool_check
from engine.flow.executor.next_step_prompt import next_step_prompt
import os
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.utils.chat_formatter import create_chat_message
from engine.tool_framework.tool_caller import ToolCaller
from engine.tool_framework.tool_registry import ToolRegistry
from memory.plan_memory.plan_memory import PlanContextMemory
from metacognitive.stream.stream import output_stream
from engine.flow.planner.tool_base_planner import tool_base_planner
from memory.episodic_memory.episodic_memory import store_long_pass_memory
import uuid
import copy

registry = ToolRegistry()
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
tools_dir = os.path.join(project_root, "tools")
registry.scan_directory(tools_dir)
tool_caller_client = ToolCaller(registry)

plan_context_memory = PlanContextMemory()
short_term_memory = ShortTermMemory()
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")
INTERACTION_MODE = os.environ.get("INTERACTION_MODE", "terminal")

def execute_intent_chain(
    user_intent: str,
    messages_history: list,
    user_id: str,
    ch_id: str
):   
    output_stream(log=f"No experience for {user_intent}...", user_id=user_id, type="think", ch_id=ch_id)
    output_stream(log="Creating new execution plan ...", user_id=user_id, type="steps", ch_id=ch_id)
    plan = create_execution_plan(user_intent, user_id, ch_id)
    return process_tool_execution_plan(
        plan, messages_history, user_id, user_intent, ch_id
    )

def process_tool_execution_plan(plan, messages_history: list, user_id: str, user_intent: str, ch_id: str):
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
    found_tools = []
    for step in plan:
        output_stream(log=f"Finding appropriate tool for step: {step['intent']}...", user_id=user_id, type="steps", ch_id=ch_id)
        found_tools.extend(resolve_tool_for_step(step))

    #replan
    found_tools = get_unique_tools(found_tools)
    if(len(found_tools) == 0):
        raise Exception("failed to find tools")
    output_stream(log="Making new plan based on current tools...", user_id=user_id, type="steps", ch_id=ch_id)
    plan = tool_base_planner(user_intent, found_tools, user_id, ch_id)
    # print(f"plan: {plan}")
            
    if(plan["status"] == "failed"):
        output_stream(log="Failed to make plan with current tools...", user_id=user_id, type="think", ch_id=ch_id)
        return plan
    plan = plan["plan"]
    execution_steps = "\n".join([f"execution tool: {step['tool']}\nstep purpose: {step['step purpose']}" for step in plan])
    output_stream(log=execution_steps, user_id=user_id, type="think", ch_id=ch_id)

    # Execute tools for each plan step
    process_plan_execution(messages_history, plan, user_id, ch_id)
    all_steps_executed = all(step.get("executed", False) for step in plan)
    if all_steps_executed:
        plan_context = copy.deepcopy(plan)
        for step in plan_context:
            step.pop('tool_executed_result', None)
            step.pop('executed', None)
        metadata = {
            "execution_records": plan_context
        }
        store_long_pass_memory(id=str(uuid.uuid4()), memory=user_intent, metadata=metadata, uid=user_id)
    return plan

def get_unique_tools(found_tools):
    unique_tools = []
    tool_ids = set()
    for tool in found_tools:
        tool_id = tool['id']
        if tool_id and tool_id not in tool_ids:
            tool_ids.add(tool_id)
            unique_tools.append(tool)
    return unique_tools

def process_plan_execution(messages_history, plan_steps, user_id: str, ch_id: str = ""):
    # tool_results = []
    for step_index, step in enumerate(plan_steps):
        # if not step.get("tool_necessity", True):
        output_stream(log=f"Executing step: {step['step purpose']}...", user_id=user_id, type="steps", ch_id=ch_id)
        #     continue
        if step.get("executed", False):
            continue
            
        tool_result = execute_step_tool(
            messages_history,
            step,
            plan_steps,
            user_id,
            ch_id,
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
    
def validate_step_necessity(step, plan, messages_history, done_steps):
    """Check if a step is necessary to execute"""
    result = step_tool_check(plan, step, messages_history, done_steps)
    return extract_json_from_str(result)

def resolve_tool_for_step(step):
    """Find appropriate tool for a step from memory"""
    memories = retrieve_short_pass_memory(step["description"])
    if not memories:
        return False
    return memories["matches"]

def execute_step_tool(messages_history,step, plan_steps, user_id: str, ch_id: str, step_index: int):
    """
    Execute tool for a plan step
    
    Returns:
        str: Tool execution record if successful, None otherwise
    """
    tool_config = parse_tool_config(step)
    
    def execute_with_config(messages_history):
        reply_json = validate_tool_parameters(
            tool_config,
            messages_history, 
            plan_steps,
            step,
            user_id,
            ch_id
        )
        
        if not reply_json["can_proceed"]:
            return {
                "toolName": step["tool"],
                "result": f"Please input required arguments to continue: {reply_json['missing_required_arguments']}", 
                "status": "need_input"
            }
            
        execution_result = execute_tool_operation(tool_config, reply_json, user_id, ch_id)
        if execution_result == {"status": "failure"}:
            return {
                "toolName": step["tool"],
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
            method_metadata = extract_json_from_str(step['data'])
            # print(f" - method_metadata: {method_metadata} - \n")
            if method_metadata['inputs']:
                for input in method_metadata['inputs']:
                    
                    try:
                        if isinstance(input, dict):
                            append_input_param = reply_json['extracted_arguments']['required_arguments'][input['name']]
                            del append_input_param['value']
                            input.update(append_input_param)
                    except:
                        append_input_param = {}
                        input.update(append_input_param)
                step['data'] = method_metadata
            return {
                "toolName": step["tool"],
                "result": execution_result,
                "status": "success"
            }
        return None
    
    return execute_with_config(messages_history)

def parse_tool_config(tool):
    tool_dict = extract_json_from_str(tool["data"])
    tool_name =tool["tool"]
    tool_dict["tool"] = tool_name
    return tool_dict

def validate_tool_parameters(tool_config, messages_history, plan_steps, step, user_id, ch_id):
    """Attempt to execute tool with current configuration"""
    print(f"tool_config: {tool_config}")
    print(f"messages_history: {step}")
    next_step_content = next_step_prompt(plan_steps, tool_config, messages_history)
    prompt = [{"role": "user", "content": next_step_content}]
    
    reply = chat_completion(prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0}, user_id=user_id, ch_id=ch_id)
    reply_json = extract_json_from_str(reply)
    print(f"reply_json: {reply_json}")
    return reply_json

def execute_tool_operation(tool_config, reply_json, user_id, ch_id):
    """Execute tool with provided arguments"""
    args = {}
    required_args = reply_json.get("extracted_arguments", {}).get("required_arguments", {})
    for arg_name, arg_info in required_args.items():
        args[arg_name] = arg_info.get("value", {})
    result,_ = execute_tool(
        tool_caller_client,
        tool_config['tool'],
        tool_config['method'],
        args,
        user_id,
        ch_id
    )
    
    # if verify_tool_execution(tool_config, result, user_id, ch_id) == "success":
    #     return result
    # return {"status": "failure"}
    return {"status": "success"}

def handle_user_input(user_id: str):
    """Handle failed tool execution by requesting user input"""
    user_input = input("Please input required arguments to continue: ")
    if not user_input:
        return False
    short_term_memory.add_context(create_chat_message("user", user_input), user_id)
    return True
