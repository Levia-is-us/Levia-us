import os
import sys
import dotenv

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from engine.flow.evaluator.evaluator_docgen_flow import evaluator_docgen_flow

code = """
def calculate(expression: str) -> float:
    # Evaluates a mathematical expression string and returns the calculated result.

    # Args:
    #     expression (str): A string containing a valid mathematical expression
    #                      e.g. "2 + 3 * 4", "10 / 2", etc.

    # Returns:
    #     float: The calculated result of evaluating the expression

    # Warning:
    #     This function uses eval() which can be unsafe if the input is not properly sanitized.
    #     Only use with trusted input expressions.
    return eval(
        expression
    ) 
"""

xml = evaluator_docgen_flow(code)
print(xml)
