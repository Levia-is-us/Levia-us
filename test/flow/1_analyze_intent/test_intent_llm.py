from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import os
from pathlib import Path
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

from engine.flow.handle_intent_flow.analyze_intent_flow import handle_intent_flow


models = [
    "claude-3-5-sonnet",
    # "claude-3-7-sonnet-20250219",
    # "deepseek-v3",
    # "deepseek-r1",
    # "gpt-4o-mini",
]


def load_test_cases():
    """Load test case files"""
    case_path = Path(__file__).parent / "cases.yml"
    with open(case_path, "r") as f:
        data = yaml.safe_load(f)
    return data["test_cases"]


def run_single_test(model, user_input, idx):
    """Run a single test case and return the result"""
    os.environ["CHAT_MODEL_NAME"] = model
    start = int(time.time())
    try:
        output = handle_intent_flow(
            chat_messages=[],
            input_message=user_input,
            user_id=f"user-{idx}",
        )
    except Exception as e:
        output = f"Error in model [{model}] for input [{user_input}]: {str(e)}"
    end = int(time.time())
    return output, round((end - start), 2)


def print_test_result(model, user_input, output, exec_ret, exec_time):
    """Format and print test result"""

    # ANSI color codes
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    if "Failed" in exec_ret:
        msg = f"{RED}Execution result: {exec_ret}{RESET}"
    else:
        msg = f"{GREEN}Execution result: {exec_ret}{RESET}"

    type = output.get("type", None) if isinstance(output, dict) else None

    print(f"{'-'*100}")
    print(f"🔶  {msg}")
    print(f"🤖  Model: {model}")
    print(f"📝  Input: {user_input}")
    print(f"📊  Output: {output}")
    print(f"🏷️  Type: {type}")
    print(f"⏱️  Execution time: {exec_time} seconds")


def calculate_model_statistics(results):
    """Calculate statistics for each model's execution times"""
    model_stats = {}

    for model in models:
        model_times = [r["execution_time"] for r in results if r["model"] == model]
        failed_count = len(
            [r for r in results if r["model"] == model and "Failed" in r["exec_ret"]]
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


def save_results_to_json(results):
    """Save test results and statistics to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Calculate statistics
    model_stats = calculate_model_statistics(results)

    # Get failed cases for each model
    failed_cases = {}
    for model in models:
        failed_cases[model] = [
            r for r in results if r["model"] == model and "Failed" in r["exec_ret"]
        ]

    # Group results by model
    results = {model: [r for r in results if r["model"] == model] for model in models}

    # Combine results and stats
    final_results = {
        "model_statistics": model_stats,
        "failed_cases": failed_cases,
        "test_results": results,
    }

    save_path = Path(__file__).parent / f"intent_test_results_{timestamp}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to: {save_path}")


def check_output_format(output):
    """Check the output of a single test case for required fields and validity"""
    issues = []

    if not isinstance(output, dict):
        issues.append("output is not a dictionary")
        return " | ".join(issues)

    # Check if output exists
    if output is None:
        issues.append("output is None")
        return " | ".join(issues)

    # Check for required fields
    required_fields = ["type", "intent", "response"]
    for field in required_fields:
        if field not in output:
            issues.append(f"missing required field: {field}")

    # Exit early if type is missing as we need it for further checks
    if "type" not in output:
        return " | ".join(issues)

    # Check if type is valid
    intent_type = output["type"]
    valid_types = ["direct_answer", "call_tools"]
    if intent_type not in valid_types:
        issues.append(
            f'invalid type: {intent_type} (expected: {" or ".join(valid_types)})'
        )

    # Check for call_tools specific requirements
    if intent_type == "call_tools" and "short-intent" not in output:
        issues.append("missing field: short-intent (required for call_tools type)")

    # Return aggregated issues or success message
    return " | ".join(issues) if issues else None


def check_case_fail(output, expected_type, format_issues):
    """Check if a test case failed"""

    if not isinstance(output, dict):
        return f"Failed: {output}"

    output_type = output.get("type", None)
    if output_type != expected_type:
        return f"Failed: output type {output_type} does not match expected type {expected_type}"
    if format_issues:
        return f"Failed: output format issues - {format_issues}"
    return f"Passed"


def linear_execute(cases: list):
    """Linearly execute test cases"""
    idx = 1
    results = []

    # For each test case, test with all models
    for test_case in cases:
        expected_type = test_case["expect"][type]
        for model in models:
            user_input = test_case["input"]
            output, exec_time = run_single_test(model, user_input, idx)
            # Check output format and case failure
            format_issues = check_output_format(output)
            exec_ret = check_case_fail(output, expected_type, format_issues)
            # Print test result
            print_test_result(model, user_input, output, exec_ret, exec_time)

            # Store result for JSON export
            result_entry = {
                "model": model,
                "user_input": user_input,
                "output": output,
                "exec_ret": exec_ret,
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
            model, user_input, output, exec_ret, exec_time, _ = future.result()
            print_test_result(model, user_input, output, exec_ret, exec_time)

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
    user_input = test_case["input"]
    output, exec_time = run_single_test(model, user_input, idx)

    # Check output format and case failure
    expected_type = test_case["expect"]["type"]
    format_issues = check_output_format(output)
    exec_ret = check_case_fail(output, expected_type, format_issues)

    # Store result for JSON export
    with result_lock:
        result_entry = {
            "model": model,
            "user_input": user_input,
            "output": output,
            "exec_ret": exec_ret,
            "execution_time": exec_time,
            "case_idx": task_key[0],
            "model_idx": task_key[1],
        }
        results.append(result_entry)

    return model, user_input, output, exec_ret, exec_time, task_key


def test_intent_llm(is_concurrent=True):
    """
    Test the intent handling capability of different models

    Load test cases and run all test cases for each model, printing results for analysis
    """
    test_cases = load_test_cases()
    # Get all test cases
    cases = [user_input for case_set in test_cases for user_input in case_set["cases"]]

    if not is_concurrent:
        # Execute test cases linearly
        linear_execute(cases)
    else:
        # Execute test cases concurrently
        concurrent_execute(cases)


if __name__ == "__main__":
    test_intent_llm()
