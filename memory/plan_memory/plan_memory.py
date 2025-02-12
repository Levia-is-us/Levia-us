from memory.plan_memory.plan_memory_provider.local_plan_context_store.local_context_store import (
    LocalContextStore,
)
from memory.plan_memory.plan_memory_provider.base_context import PlanStatus


class PlanContextMemory:
    def __init__(self, max_length: int = 1000):
        self.context_store = LocalContextStore(max_length)

    def create_plan_context(self, plan_steps: list, user_key: str = "local"):
        self.context_store.create_plan_context(plan_steps, user_key)

    def get_current_plan_context(self, user_key: str = "local"):
        return self.context_store.get_current_plan_context(user_key)
    
    def update_step_status_context(self, status: PlanStatus, user_key: str = "local"):
        self.context_store.update_step_status_context(status, user_key)

    def reset_plan_context(self, user_key: str = "local"):
        self.context_store.reset_plan_context(user_key)

    def delete_plan_context(self, user_key: str = "local"):
        self.context_store.delete_plan_context(user_key)
