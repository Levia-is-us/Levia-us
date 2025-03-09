from memory.db_connection.mysql_connector import MySQLPool
from engine.flow.executor.check_tools_result_prompt import check_tools_result_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
from engine.tool_framework.tool_caller import ToolCaller
from metacognitive.stream.stream import output_stream
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

db_pool = MySQLPool()


def execute_tool(
    tool_caller: ToolCaller, tool_name: str, tool_method: str, tool_args: dict, user_id: str, ch_id: str
):
    """Execute tool and record results"""
    output_stream(log=f"Running {tool_name}...", user_id=user_id, type="think", ch_id=ch_id)

    execution_record = {"tool": tool_name, "method": tool_method, "args": tool_args}

    try:
        result = tool_caller.call_tool(
            tool_name=tool_name, method=tool_method, kwargs=tool_args
        )
        # if isinstance(result, dict):
        #     return {"status": "failure", "result": "tool execution result is invalid"}, None
        status = verify_tool_execution(execution_record, result, user_id, ch_id)
        record_tool_execution(tool_name, tool_method, tool_args, result)
        output_stream(log=f"{result}", user_id=user_id, type="think", ch_id=ch_id, title="tool execution result")

        return result, create_execution_record(
            tool_name, tool_method, tool_args, result, status
        )
    except Exception as e:
        print(f"\033[91mexecute_tool error: {str(e)}\033[0m")
        return {"status": "failure", "result": str(e)}, None


def verify_tool_execution(execution_record: dict, result: dict, user_id: str, ch_id: str) -> str:
    """Verify tool execution result using LLM"""
    # if result["status"] == "failure":
    #     return "failure"
    llm_check_prompt = check_tools_result_prompt(
        tool_execution=str(execution_record), tool_output=result
    )

    llm_confirmation = chat_completion(
        llm_check_prompt, model=CHAT_MODEL_NAME, config={"temperature": 0}, user_id=user_id, ch_id=ch_id
    )

    llm_confirmation = extract_json_from_str(llm_confirmation)
    # todo: add error handling
    return "failure" if llm_confirmation["status"] == "failure" else "success"


def record_tool_execution(tool_name: str, tool_method: str, args: dict, result: dict):
    """Record tool execution in database"""
    sql = """
        INSERT INTO levia_tool_executor_history 
        (toolId, uid, tool_execute_args, tool_response, createTime) 
        VALUES (%s, %s, %s, %s, now())
    """
    tool_id = tool_name + tool_method
    db_pool.execute(sql, (tool_id, "123", str(args), str(result)))


def create_execution_record(
    tool_name: str, tool_method: str, args: dict, result: dict, status: str
) -> str:
    """Create execution record string"""
    return str(
        {
            "tool": tool_name,
            "method": tool_method,
            "args": args,
            "result": result,
            "status": status,
        }
    )
