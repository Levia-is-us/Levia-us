from memory.plan_memory.plan_memory_provider.local_plan_context_store.local_context_store import (
    PlanContextStore,
)
import threading
from memory.plan_memory.plan_memory_provider.base_context import PlanStatus


class PlanContextMemory:
    _instance = None
    _lock = threading.Lock()  # Ensuring thread safety

    def __new__(cls):
        with cls._lock:  # Thread-safe instantiation
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the context store."""
        self.context_store = PlanContextStore()

    def create_plan_context(self, plan_steps: list, user_key: str = "local"):
        self.context_store.create_plan_context(plan_steps, user_key)

    def get_current_plan_context(self, user_key: str = "local"):
        return self.context_store.get_current_plan_context(user_key)
    
    def reset_plan_context(self, user_key: str = "local"):
        self.context_store.reset_plan_context(user_key)

    def delete_plan_context(self, user_key: str = "local"):
        self.context_store.delete_plan_context(user_key)
    
    def update_step_status_context(self, step_index: int, tool_necessity: bool = True, execution_tool: dict = None, execution_result: dict = None, executed: bool = False, user_key: str = "local"):
        self.context_store.update_step_status_context(step_index, tool_necessity, execution_tool, execution_result, executed, user_key)

    def advance_step_context(self, user_key: str = "local"):
        self.context_store.advance_step_context(user_key)

    def get_current_step_context(self, user_key: str = "local"):
        return self.context_store.get_current_step_context(user_key)
