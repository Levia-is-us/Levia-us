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
    
from engine.flow.planner.planner import create_execution_plan

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")



if __name__ == "__main__":
    """put your intent here"""
    intent = input("Enter your intent: ")
    # plan = create_execution_plan(intent) + context
    plan = create_execution_plan(intent)
    print(f"plan: {plan}")


