import os
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.tool_framework.tool_caller import ToolCaller
from engine.tool_framework.tool_registry import ToolRegistry
from memory.plan_memory.plan_memory import PlanContextMemory
from engine.flow.executor.short_chain_executor import execute_intent_chain
from engine.flow.episodic_memory_handle_flow.episodic_memory_executor import episodic_memory_executor

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
    task_in_process,res = episodic_memory_executor(user_id, user_intent, chat_messages)
    if task_in_process:
        return res

    return execute_intent_chain(
        user_intent, chat_messages, user_id
    )
