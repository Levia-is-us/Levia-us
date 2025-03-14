from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import os
from pathlib import Path
from collections import Counter
import sys
import threading
import time
import yaml

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from engine.flow.executor.transform_code_llm import transformation_code_llm


models = [
    "claude-3-7-sonnet-20250219",
    # "deepseek-v3",
    # "deepseek-r1",
    # "gpt-4o-mini",
]


def load_test_cases():
    """Load test case files"""
    case_path = Path(__file__).parent / "transform_code_llm_cases.yml"
    with open(case_path, "r") as f:
        data = yaml.safe_load(f)
    return data["test_cases"]


def run_single_test(model, test_case, idx):
    """Run a single test case and return the result"""
    os.environ["CHAT_MODEL_NAME"] = model
    input_structure = test_case["input_structure"]
    output_structure = test_case["output_structure"]
    start = time.time()
    try:
        output = transformation_code_llm(
            input_structure, output_structure, user_id=f"user-{idx}", ch_id=f"ch-{idx}"
        )
    except Exception as e:
        output = f"Error in model [{model}] for input [{test_case['input']}: {str(e)}"
    end = time.time()
    return output, round((end - start), 2)


def linear_execute(cases: list):
    """Linearly execute test cases"""
    idx = 1
    results = []

    # For each test case, test with all models
    for test_case in cases:
        for model in models:
            output, exec_time = run_single_test(model, test_case, idx)
            # Check if case failed
            exec_ret = check_case_fail(output, test_case)
            # Print test result
            print_test_result(
                model,
                test_case["input_structure"],
                test_case["output_structure"],
                output,
                exec_ret,
                exec_time,
            )

            # Store result for JSON export
            result_entry = {
                "model": model,
                "input_structure": test_case["input_structure"],
                "output_structure": test_case["output_structure"],
                "output": output,
                "execution_result": exec_ret,
                "execution_time": exec_time,
            }
            results.append(result_entry)
            idx += 1

    # Save results to JSON file
    save_results_to_json(results)


def concurrent_execute(cases: list):
    """Execute test cases concurrently"""
    idx = 1
    results = []
    result_lock = threading.Lock()
    tasks = []
    idx_map = {}  # Used to record the original index of each task

    # Generate tasks for all cases and models
    for case_idx, test_case in enumerate(cases):
        for model_idx, model in enumerate(models):
            task_key = (case_idx, model_idx)
            tasks.append((model, test_case, idx, task_key))
            idx_map[task_key] = idx
            idx += 1

    # Use ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit tasks to executor
        future_to_task = {
            executor.submit(
                run_single_test_task,
                model,
                test_case,
                task_idx,
                result_lock,
                results,
                task_key,
            ): (model, test_case, task_idx, task_key)
            for model, test_case, task_idx, task_key in tasks
        }

        # Print results as they are completed
        for future in as_completed(future_to_task):
            model, input_structure, output_structure, output, exec_ret, exec_time, _ = (
                future.result()
            )
            print_test_result(
                model,
                input_structure,
                output_structure,
                output,
                exec_ret,
                exec_time,
            )

    # Sort results by case index and model index
    sorted_results = sorted(results, key=lambda x: (x["case_idx"], x["model_idx"]))

    # Delete case_idx and model_idx from results
    for result in sorted_results:
        del result["case_idx"]
        del result["model_idx"]

    # Save results to JSON file
    save_results_to_json(sorted_results)


def run_single_test_task(model, test_case, idx, result_lock, results, task_key):
    """Run a single test task in a thread and return the result"""
    output, exec_time = run_single_test(model, test_case, idx)
    input_structure = test_case["input_structure"]
    output_structure = test_case["output_structure"]

    # Check if case failed
    exec_ret = check_case_fail(output, test_case)

    # Store result for JSON export
    with result_lock:
        result_entry = {
            "model": model,
            "input_structure": input_structure,
            "output_structure": output_structure,
            "output": output,
            "execution_result": exec_ret,
            "execution_time": exec_time,
            "case_idx": task_key[0],
            "model_idx": task_key[1],
        }
        results.append(result_entry)
    return model, input_structure, output_structure, output, exec_ret, exec_time, task_key


def calculate_model_statistics(results):
    """Calculate statistics for each model's execution times"""
    model_stats = {}

    for model in models:
        model_times = [r["execution_time"] for r in results if r["model"] == model]
        failed_count = len(
            [r for r in results if r["model"] == model and "Failed" in r["execution_result"]]
        )
        if model_times:
            model_stats[model] = {
                "avg_time": round(sum(model_times) / len(model_times), 2),
                "min_time": min(model_times),
                "max_time": max(model_times),
                "total_cases": len(model_times),
                "failed_cases": failed_count,
                "failed_rate": round(failed_count / len(model_times), 2),
            }

    print("\n" + "-" * 100)
    print("Model Performance Statistics:")
    for model, stats in model_stats.items():
        print(f"\nModel: {model}")
        print(f"Average Time: {stats['avg_time']} seconds")
        print(f"Minimum Time: {stats['min_time']:.2f} seconds")
        print(f"Maximum Time: {stats['max_time']:.2f} seconds")
        print(f"Total Test Cases: {stats['total_cases']}")
        print(f"Failed Cases: {stats['failed_cases']}")
        print(f"Failed Rate: {stats['failed_rate']}")
        print("\n" + "-" * 100)

    return model_stats


def normalize_booleans(obj):
    """
    Recursively normalize string boolean values 'true'/'false' to Python's True/False
    
    Args:
        obj: Any Python object that might contain string boolean values
        
    Returns:
        Object with normalized boolean values
    """
    if isinstance(obj, dict):
        return {k: normalize_booleans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_booleans(item) for item in obj]
    elif obj == "true":
        return True
    elif obj == "false":
        return False
    else:
        return obj

def validate_transformation_function(actual_code, input_str, expected_output_str):
    """
    Validate if a transformation function correctly implements the expected conversion
    
    Args:
        actual_code: Generated function code as string
        input_str: Input JSON string
        expected_output_str: Expected output JSON string
    
    Returns:
        bool: True if the function works as expected, False otherwise
    """
    try:
        # Parse input and expected output
        input_data = json.loads(input_str)
        expected_output = json.loads(expected_output_str)
        
        # Handle boolean representation differences between YAML and JSON
        expected_output = normalize_booleans(expected_output)
        
        # Create local namespace to execute function code
        local_namespace = {}
        exec(actual_code, {}, local_namespace)
        
        # Get the transform function
        if "transform" not in local_namespace:
            return False
        
        transform_func = local_namespace["transform"]
        
        # Execute the function to get actual output
        actual_output = transform_func(input_data)
        
        # Also normalize boolean values in the output
        actual_output = normalize_booleans(actual_output)
        
        # Check if output matches expected result
        # 1. Check type
        if not isinstance(actual_output, type(expected_output)):
            return False
        
        # 2. Check content - for lists, consider that dictionary values may have undefined order
        if isinstance(expected_output, list):
            # Compare length
            if len(actual_output) != len(expected_output):
                return False
                
            # If all elements in the list are equal (regardless of order)
            if Counter(actual_output) == Counter(expected_output):
                return True
                
            # If order should also match
            if actual_output == expected_output:
                return True
                
            # Special handling for this case - check if ordering follows pattern
            # Example output should be [1, "Alice", 2, "Bob"]
            valid_order = True
            for i in range(0, len(actual_output), 2):
                if i+1 < len(actual_output):
                    if not (isinstance(actual_output[i], (int, float)) and isinstance(actual_output[i+1], str)):
                        valid_order = False
                        break
            
            if valid_order:
                # Validate all (id, name) pairs are correct
                pairs_actual = [(actual_output[i], actual_output[i+1]) for i in range(0, len(actual_output), 2)]
                pairs_expected = [(expected_output[i], expected_output[i+1]) for i in range(0, len(expected_output), 2)]
                
                if set(pairs_actual) == set(pairs_expected):
                    return True
            
            return False
        
        # For dictionaries, special handling for string "true"/"false" vs boolean True/False comparison
        elif isinstance(expected_output, dict):
            for key, expected_val in expected_output.items():
                if key not in actual_output:
                    return False
                
                actual_val = actual_output[key]
                
                # Special handling for boolean string representation
                if isinstance(expected_val, bool) and isinstance(actual_val, str):
                    if (expected_val is True and actual_val.lower() == "true") or \
                       (expected_val is False and actual_val.lower() == "false"):
                        continue
                
                # Special handling for numeric string representation
                elif isinstance(expected_val, (int, float)) and isinstance(actual_val, str):
                    try:
                        if float(actual_val) == float(expected_val):
                            continue
                    except ValueError:
                        return False
                
                # Direct comparison for other cases
                elif actual_val != expected_val:
                    return False
            
            # Check if all keys have been processed
            for key in actual_output:
                if key not in expected_output:
                    return False
            
            return True
        
        # For other types of output, compare directly
        return actual_output == expected_output
            
    except Exception as e:
        print(f"Error in validation: {e}")
        return False

def check_case_fail(output, test_case):
    """Check case failure based on output format and expect"""
    # Basic input validation
    if output is None:
        return "Failed: output is None"

    if not output.startswith("def "):
        return "Failed: output is not a function"

    # Validate transformation function output
    is_work = validate_transformation_function(
        output, test_case["input_structure"], test_case["output_structure"]
    )

    if is_work:
        return "Passed"
    else:
        return "Failed: output does not match expected transformation"


def print_test_result(
    model, input_structure, output_structure, output, exec_ret, exec_time
):
    """Format and print test result"""

    # ANSI color codes
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    if "Failed" in exec_ret:
        msg = f"{RED}Execution result: {exec_ret}{RESET}"
    else:
        msg = f"{GREEN}Execution result: {exec_ret}{RESET}"

    print(f"{'-'*100}")
    print(f"🔶  {msg}")
    print(f"🤖  Model: {model}")
    print(f"📝  InputStructure: {input_structure}")
    print(f"📝  OutputStructure: {output_structure}")
    print(f"📊  Output: {output}")
    print(f"⏱️  Execution time: {exec_time} seconds")


def save_results_to_json(results):
    """Save test results and statistics to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Calculate statistics
    model_stats = calculate_model_statistics(results)

    # Get failed cases for each model
    failed_cases = {}
    for model in models:
        failed_cases[model] = [
            r for r in results if r["model"] == model and "Failed" in r["execution_result"]
        ]

    # Group results by model
    results = {model: [r for r in results if r["model"] == model] for model in models}

    # Combine results and stats
    final_results = {
        "model_statistics": model_stats,
        "failed_cases": failed_cases,
        "test_results": results,
    }

    save_path = Path(__file__).parent / f"transform_code_test_{timestamp}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to: {save_path}")


def main(is_concurrent=True):
    """Run test cases for episodic check LLM"""
    # Get all test cases
    cases = load_test_cases()

    if not is_concurrent:
        # Execute test cases linearly
        linear_execute(cases)
    else:
        # Execute test cases concurrently
        concurrent_execute(cases)


if __name__ == "__main__":
    main()
