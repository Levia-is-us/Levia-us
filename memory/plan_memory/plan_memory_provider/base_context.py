import abc
from memory.plan_memory.plan_memory_provider.local_plan_context_store.local_context_store import PlanStatus

class BaseContextStore(abc.ABC):
    @abc.abstractmethod
    def create_plan_context(self, plan_steps: list, user_key: str = "local"):
        pass
    @abc.abstractmethod
    def get_current_plan_context(self, user_key: str = "local"):
        pass
    @abc.abstractmethod
    def update_step_status_context(self, status: PlanStatus, user_key: str = "local"):
        pass
    @abc.abstractmethod
    def reset_plan_context(self, user_key: str = "local"):
        pass
    @abc.abstractmethod
    def delete_plan_context(self, user_key: str = "local"):
        pass