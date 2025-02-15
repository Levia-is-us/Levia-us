from engine.utils.memory_filter import filter_memories_by_score
from memory.episodic_memory.episodic_memory import retrieve_long_pass_memory
from engine.flow.planner.planner import check_plan_sufficiency
from engine.flow.executor.tool_executor import execute_tool
from engine.utils.json_util import extract_json_from_str
from engine.tool_framework.tool_caller import ToolCaller
from engine.tool_framework.tool_registry import ToolRegistry
import os
registry = ToolRegistry()
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
print(f"registry project_root: {project_root}")
tools_dir = os.path.join(project_root, "tools")
registry.scan_directory(tools_dir)
tool_caller_client = ToolCaller(registry)

def long_chain_executor(user_id: str, user_intent: str, chat_messages: list):
    memories = retrieve_long_pass_memory(user_intent)
    high_score_memories = filter_memories_by_score(memories)
    top_memory = high_score_memories[0]
    try:
        execution_records = [
            eval(record) for record in top_memory["metadata"]["execution_records"]
        ]
        if check_plan_sufficiency(user_intent, top_memory["id"], execution_records):
            res = execute_existing_records(execution_records)
            return str(res)
    except Exception as e:
        print(f"execute existing records error: {str(e)}")

def execute_existing_records(execution_records: list) -> dict:
    """Execute existing tool records"""
    for record in execution_records:
        try:
            if isinstance(record, str):
                record = extract_json_from_str(record)
            result, _ = execute_tool(
                tool_caller_client, record["tool"], record["method"], record["args"]
            )
            print(f"Executed tool: {record['tool']}.{record['method']}")
            print(f"Result: {result}")
            return result
        except Exception as e:
            print(f"Error processing execution record: {str(e)}")
            raise e
