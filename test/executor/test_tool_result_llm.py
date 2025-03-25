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
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

sys.path.insert(0, project_root)

from engine.flow.executor.execute_tool_flow import verify_tool_execution


models = [
    "claude-3-7-sonnet-20250219",
    # "deepseek-v3",
    # "deepseek-r1",
    # "gpt-4o-mini",
]


def load_test_cases():
    """Load test case files"""
    case_path = Path(__file__).parent / "cases.yml"
    with open(case_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["test_cases"]


def run_single_test(model, test_case, idx):
    """Run a single test case and return the result"""
    os.environ["CHAT_MODEL_NAME"] = model
    execution_record = test_case["execution_record"]
    result = test_case["result"]
    start = time.time()
    try:
        output = verify_tool_execution(
            execution_record, result, user_id=f"user-{idx}", ch_id=f"ch-{idx}"
        )
    except Exception as e:
        output = f"Error in model [{model}] for intent [{test_case}]: {str(e)}"
    end = time.time()
    return output, round((end - start), 2)


def linear_execute(cases: list):
    """Linearly execute test cases"""
    idx = 1
    results = []

    # For each test case, test with all models
    for test_case in cases:
        expect = test_case["expect"]
        for model in models:
            output, exec_time = run_single_test(model, test_case, idx)
            # Check case failure
            exec_ret = check_case_fail(output, expect)
            # Print test result
            print_test_result(model, test_case, output, exec_time)

            # Store result for JSON export
            result_entry = {
                "model": model,
                "intent": test_case,
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
            model, intent, output, exec_ret, exec_time, _ = future.result()
            print_test_result(model, intent, output, exec_ret, exec_time)

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
    # Check case failure
    exec_ret = check_case_fail(output, test_case["expect"])

    # Store result for JSON export
    with result_lock:
        result_entry = {
            "model": model,
            "intent": test_case,
            "output": output,
            "execution_result": exec_ret,
            "execution_time": exec_time,
            "case_idx": task_key[0],
            "model_idx": task_key[1],
        }
        results.append(result_entry)
    return model, test_case, output, exec_ret, exec_time, task_key


def calculate_model_statistics(results):
    """Calculate statistics for each model's execution times"""
    model_stats = {}

    for model in models:
        model_times = [r["execution_time"] for r in results if r["model"] == model]
        failed_count = len(
            [
                r
                for r in results
                if r["model"] == model and "Failed" in r["execution_result"]
            ]
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


def check_case_fail(output, expect):
    """Check case failure based on output format and expect"""
    # Basic input validation
    if output is None:
        return "Failed: output is None"

    if output != expect:
        return f"Failed: output {output} does not match expected value {expect}"
    
    return "Passed"


def print_test_result(model, intent, output, exec_ret, exec_time):
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
    print(f"📝  Intent: {intent}")
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

    save_path = Path(__file__).parent / f"tool_result_test_{timestamp}.json"

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
