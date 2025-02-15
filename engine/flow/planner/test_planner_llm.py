import sys
import os
import json

# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (4 levels up)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from engine.flow.planner.planner import create_execution_plan

if __name__ == "__main__":
    """put your intent here"""
    # intent = input("Enter your intent: ")
    intent = "The user wants to search for today's football news."
    # plan = create_execution_plan(intent) + context
    plan = create_execution_plan(intent)
    # save to file
    with open("plan.txt", "w") as f:
        f.write(json.dumps(plan, indent=4))
    print(f"plan: {plan}")
