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
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.utils.chat_formatter import create_chat_message
from engine.tool_framework.tool_caller import ToolCaller
from engine.tool_framework.tool_registry import ToolRegistry
from memory.plan_memory.plan_memory import PlanContextMemory
from metacognitive.stream.stream import output_stream
from engine.flow.executor.episodic_memory_executor import episodic_memory_executor
from engine.flow.executor.short_chain_executor import execute_intent_chain
import time

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
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")
INTERACTION_MODE = os.environ.get("INTERACTION_MODE", "terminal")

def chat_executor(user_id: str, user_intent: str, chat_messages: list):
    print("\033[93mRecalling similar scenes from episodic memory...\033[0m")
    # task_in_process,res = long_chain_executor(user_id, user_intent, chat_messages)
    # if task_in_process:
    #     return res

    return execute_intent_chain(
        user_intent, chat_messages, user_id
    )
