from engine.utils.memory_filter import filter_memories_by_score
from engine.flow.planner.planner import check_plan_sufficiency
from engine.flow.executor.tool_executor import execute_tool
from engine.utils.json_util import extract_json_from_str
from engine.tool_framework.tool_caller import ToolCaller
from engine.tool_framework.tool_registry import ToolRegistry
import os
from metacognitive.stream.stream import output_stream
from memory.plan_memory.plan_memory import PlanContextMemory
from engine.flow.episodic_memory_handle_flow.episodic_check import episodic_check
from engine.flow.executor.next_step_prompt import next_step_prompt
from engine.llm_provider.llm import chat_completion
from memory.episodic_memory.episodic_memory import retrieve_long_pass_memory, delete_long_pass_memory
from engine.flow.executor.transform_code import transform_code
registry = ToolRegistry()
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
# print(f"registry project_root: {project_root}")
tools_dir = os.path.join(project_root, "tools")
registry.scan_directory(tools_dir)
tool_caller_client = ToolCaller(registry)
plan_context_memory = PlanContextMemory()
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

def episodic_memory_executor(user_id: str, user_intent: str, chat_messages: list, ch_id: str):
    memories = retrieve_long_pass_memory(user_intent)
    high_score_memories = filter_memories_by_score(memories)
    if len(high_score_memories) == 0:
        return False, ""
    top_memory = high_score_memories[0]
    try:
        execution_records = top_memory["metadata"]["execution_records"]
        top_memory_id = top_memory["id"]
        result = episodic_check(user_intent, chat_messages, execution_records, user_id, ch_id)
        if result.get("status") != "success":
            return False, result
        plan = result.get("plan")
        res = process_tool_execution_plan(plan, user_id, chat_messages, top_memory_id, ch_id)
        all_steps_executed = all(step.get("executed", False) for step in plan)
        if not all_steps_executed:
            return False, "Plan execution failed"
        return True,str(res)
    except Exception as e:
        print(f"execute existing records error: {e.args}")
        return False, str(e)
        
def process_tool_execution_plan(plan, user_id: str, chat_messages: list, top_memory_id: str, ch_id: str):
    # Execute tools for each plan step
    process_plan_execution(plan, user_id, chat_messages, top_memory_id, ch_id)
    return plan


def process_plan_execution(plan_steps, user_id: str, chat_messages: list, top_memory_id: str, ch_id: str):
    execution_outputs = []  # Store all tool execution outputs
    if isinstance(plan_steps, str):
        plan_steps = eval(plan_steps)
    for step_index, step in enumerate(plan_steps):
        # print(f"step: {step}")
        if step.get("executed", False):
            continue
            
        # Get tool configuration and parameters
        tool_config = parse_tool_config(step)
        if not tool_config:
            continue
            
        # Process input parameters
        input_params = get_input_parameters(tool_config, execution_outputs, chat_messages, plan_steps, user_id, ch_id)
        # print(f"input_params: {input_params}")
        
        if input_params.get("status") == "need_input":
            # Save current execution state
            save_execution_state(execution_outputs, step_index, user_id, ch_id)
            step["executed"] = False
            return {"status": "need_input", "message": input_params.get("message")}
            
        # Execute tool with processed parameters
        tool_result = execute_step_tool(
            tool_config,
            plan_steps,
            user_id,
            ch_id,
            step_index,
            input_params["params"]
        )
        if isinstance(tool_result, str):
            tool_result = eval(tool_result)
        # print(f"tool_result1: {tool_result}")
        if tool_result:
            # Store output for potential future steps
            execution_outputs.append({
                "output_id": step["step"],
                "output_value": tool_result["result"]
            })
        
        step["tool_executed_result"] = tool_result["result"]
        if tool_result["status"] == "failure":
            step["executed"] = True
            print("break")
            break
        else:
            step["executed"] = True
            if input_params.get("get_param_from_llm", False):
                try:
                    delete_long_pass_memory(top_memory_id, user_id)
                except:
                    pass



def execute_step_tool(tool_config, plan_steps, user_id: str, ch_id: str, step_index: int, args: dict):
    """
    Execute tool for a plan step
    
    Returns:
        str: Tool execution record if successful, None otherwise
    """
    # tool = step["tool"]
    # tool_config = parse_tool_config(tool)
    # print(f"tool_config1: {tool_config}")
    if not tool_config:
        return None
    
    tool_name = tool_config['tool']

    def execute_with_config(args):
            
        execution_result = execute_tool_operation(tool_config, args, user_id, ch_id)
        # print(f"execution_result: {execution_result}")     
        if execution_result:
            # plan_context_memory.update_step_status_context(
            #     step_index,
            #     execution_result=execution_result,
            #     executed=True,
            #     user_key=user_id
            # )
            return {
                "toolName": tool_name,
                "result": execution_result,
                "status": "success"
            }
            
        return None
    
    return execute_with_config(args)
    
def parse_tool_config(tool):
    if isinstance(tool, str):
        tool = extract_json_from_str(tool)
    tool_dict = tool["data"]
    if isinstance(tool_dict, str):
        tool_dict = extract_json_from_str(tool_dict)
    tool_name =tool["tool"]
    tool_dict["tool"] = tool_name
    return tool_dict

def execute_tool_operation(tool_config, args, user_id, ch_id):
    """Execute tool with provided arguments"""
    result,_ = execute_tool(
        tool_caller_client,
        tool_config['tool'],
        tool_config['method'],
        args,
        user_id,
        ch_id
    )
    return result

def get_input_parameters(tool_config: dict, execution_outputs: list, messages_history: list, plan_steps: list, user_id: str, ch_id: str) -> dict:
    """Process and retrieve input parameters based on source rules"""
    
    input_specs = extract_input_specs(tool_config)
    processed_params = {}
    
    for input_spec in input_specs:
        param_value = process_parameter_source(
            input_spec, 
            execution_outputs
        )
        if param_value.get("status") == "failure":
            res = get_tool_parameters_llm(tool_config, messages_history, plan_steps, user_id, ch_id)
            if res:
                args = {}
                required_args = res.get("extracted_arguments", {}).get("required_arguments", {})
                for arg_name, arg_info in required_args.items():
                    args[arg_name] = arg_info.get("value", {})
                return {"status": "success", "params": args, "get_param_from_llm": True}
            
        if param_value.get("status") == "need_input":
            return param_value
            
        if param_value.get("value") is not None:
            processed_params[input_spec["name"]] = param_value["value"]
            
    return {"status": "success", "params": processed_params}

def process_parameter_source(input_spec: dict, execution_outputs: list) -> dict:
    """Process individual parameter based on its source configuration"""
    try:
        # If value is already provided
        if "value" in input_spec and input_spec["value"] is not None and input_spec["value"] != "":
            value = input_spec["value"]
            type_str = input_spec.get("type", "str")
            if "str" in type_str:
                value = str(value)
            elif "int" in type_str:
                value = int(value)
            elif "float" in type_str:
                value = float(value)
            elif "bool" in type_str:
                value = bool(value)
            return {"status": "success", "value": value}
            
        source_type = input_spec.get("source", [])
        method_parameter = input_spec.get("method_parameter", "")

        method = input_spec["method"]
        if method == "direct":
            output_value = find_output_value(source_type, execution_outputs)
            return {"status": "success", "value": output_value}

            # return execution_outputs
        
        # Handle different source types
        if "context" in source_type:
            return {"status": "need_input", "message": f"Need user input for {input_spec['name']}"}
            
        elif "env" in source_type:
            value = os.environ.get(input_spec['name'])
            if value:
                return {"status": "success", "value": value}
            return {"status": "failure", "message": f"Environment variable {input_spec['name']} not found"}
            
        elif "key_vault" in source_type:
            return {"status": "success", "value": "key_vault_value"}
            
        elif method_parameter and method_parameter.startswith("def"):
            try:
                local_namespace = {}
                exec(method_parameter, {}, local_namespace)
                
                func_name = method_parameter[4:method_parameter.index('(')].strip()
                func = local_namespace[func_name]
                if len(execution_outputs) > 0:
                    input_value = execution_outputs[0]["output_value"]
                    result = func(input_value)
                    return {"status": "success", "value": result}
                else:
                    return {
                        "status": "failure", 
                        "message": "No execution outputs available for function input"
                    }
                    
            except Exception as e:
                print(f"Failed to execute function: {str(e)}")
                return {
                    "status": "failure",
                    "message": f"Failed to execute function: {str(e)}"
                }
    except Exception as e:
        print(f"Invalid source configuration: {e.args}")
        return {"status": "failure", "message": "Invalid source configuration"}

def find_output_value(output_id: str, execution_outputs: list) -> any:
    """Find output value from execution history"""
    for output in execution_outputs:
        if output_id in output["output_id"]:
            return output["output_value"]
    return None

def save_execution_state(execution_outputs: list, step_index: int, user_id: str, ch_id: str):
    """Save current execution state for resumption"""
    state = {
        "execution_outputs": execution_outputs,
        "current_step": step_index,
        "user_id": user_id
    }
    print(f"Saving execution state: {state}")
    output_stream(log="Saving execution state...", user_id=user_id, type="steps", ch_id=ch_id)

def extract_input_specs(tool_config: dict) -> list[dict]:
    """Extract input specifications from tool configuration"""
    try:    
        return tool_config.get("inputs", [])
    except Exception as e:
        print(f"Error extracting input specs: {str(e)}")
        return []
    
def get_tool_parameters_llm(tool_config, messages_history, plan_steps, user_id, ch_id):
    """Attempt to execute tool with current configuration"""
    next_step_content = next_step_prompt(plan_steps, tool_config, messages_history)
    prompt = [{"role": "user", "content": next_step_content}]
    
    reply = chat_completion(prompt, model=QUALITY_MODEL_NAME, config={"temperature": 0}, user_id=user_id, ch_id=ch_id)
    reply_json = extract_json_from_str(reply)
    if not reply_json["can_proceed"]:
            return None
    reply_json = transform_code(plan_steps, reply_json, user_id, ch_id)
    return reply_json
