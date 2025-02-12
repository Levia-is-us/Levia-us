from typing import Dict, List, Optional
from enum import Enum
from memory.plan_memory.plan_memory_provider.base_context import BaseContextStore
class PlanStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class PlanContextStore(BaseContextStore):
    def __init__(self):
        """Initialize the plan context store"""
        self.plans = {}  # Store all plans
        self.current_plan = {}  # Store current active plan for each user

    def create_plan_context(self, plan_steps: list, user_key: str = "local") -> None:
        """
        Create and store a new plan
        
        Args:
            plan_steps: List of plan steps
            user_key: Key to identify user's plan
        """
        if not isinstance(plan_steps, list):
            plan_steps = eval(plan_steps)
            
        self.plans[user_key] = {
            "steps": plan_steps,
            "current_step_index": 0,
            "status": PlanStatus.NOT_STARTED,
            "execution_records": []
        }

    def get_current_plan_context(self, user_key: str = "local") -> Optional[Dict]:
        """
        Get current plan for user
        
        Args:
            user_key: Key to identify user's plan
            
        Returns:
            Current plan context or None if no plan exists
        """
        return self.plans.get(user_key)

    def get_current_step_context(self, user_key: str = "local") -> Optional[Dict]:
        """
        Get current step from plan
        
        Returns:
            Current step or None if plan is completed
        """
        plan = self.get_current_plan(user_key)
        if not plan or plan["current_step_index"] >= len(plan["steps"]):
            return None
        return plan["steps"][plan["current_step_index"]]

    def update_step_status_context(
        self, 
        step_index: int, 
        tool_necessity: bool = True,
        execution_tool: dict = None,
        execution_result: dict = None,
        executed: bool = False,
        user_key: str = "local"
    ) -> None:
        """
        Update status of a specific step
        """
        plan = self.get_current_plan(user_key)
        if not plan or step_index >= len(plan["steps"]):
            return

        step = plan["steps"][step_index]
        step["tool_necessity"] = tool_necessity
        if execution_tool:
            step["execution_tool"] = execution_tool
        if execution_result:
            step["execution_tool_result"] = execution_result
        step["executed"] = executed

    def advance_step_context(self, user_key: str = "local") -> bool:
        """
        Move to next step in plan
        
        Returns:
            True if there are more steps, False if plan is completed
        """
        plan = self.get_current_plan(user_key)
        if not plan:
            return False

        plan["current_step_index"] += 1
        if plan["current_step_index"] >= len(plan["steps"]):
            plan["status"] = PlanStatus.COMPLETED
            return False
        return True

    def add_execution_record_context(self, record: dict, user_key: str = "local") -> None:
        """Add execution record to plan"""
        plan = self.get_current_plan(user_key)
        if plan:
            plan["execution_records"].append(record)

    def set_plan_status_context(self, status: PlanStatus, user_key: str = "local") -> None:
        """Set plan status"""
        plan = self.get_current_plan(user_key)
        if plan:
            plan["status"] = status

    def reset_plan_context(self, user_key: str = "local") -> None:
        """Reset plan to initial state"""
        if user_key in self.plans:
            steps = self.plans[user_key]["steps"]
            self.create_plan(steps, user_key)

    def delete_plan_context(self, user_key: str = "local") -> None:
        """Delete plan for user"""
        if user_key in self.plans:
            del self.plans[user_key]