import sys
import os

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
)

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from engine.flow.planner.make_general_plan_flow import create_execution_plan


if __name__ == "__main__":
    """put your intent here"""
    intent = 'The user wants to know the current news headlines and stories from the United States as of March 7, 2025.'
    # plan = create_execution_plan(intent) + context
    plan = create_execution_plan(intent, user_id="local", ch_id="ch_id")
    print(f"plan: {plan}")


