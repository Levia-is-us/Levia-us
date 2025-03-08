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
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)

from engine.flow.handle_intent_flow.analyze_intent_flow import handle_intent_flow


models = [
    "claude-3-5-sonnet",
    # "claude-3-7-sonnet-20250219",
    "deepseek-r1",
    # "gpt-4.5-preview",
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
    os.environ["QUALITY_MODEL_NAME"] = model
    start = int(time.time())
    ret = handle_intent_flow(
        chat_messages=[], input_message=user_input, user_id=f"user-{idx}"
    )
    end = int(time.time())
    if not isinstance(ret, dict):
        output = None
    else:
        output = ret.get("intent", None)
    return output, end - start


def print_test_result(model, user_input, output, exec_time):
    """Format and print test result"""
    print(f"{'-'*100}")
    print(f"Model: {model}")
    print(f"Input: {user_input}")
    print(f"Output: {output}")
    print(f"Execution time: {exec_time} seconds")


def save_results_to_json(results):
    """Save test results to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    save_path = Path(__file__).parent / f"intent_test_results_{timestamp}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to: {save_path}")


def linear_execute(cases: list):
    """Linearly execute test cases"""
    idx = 1
    results = []

    # For each test case, test with all models
    for user_input in cases:
        for model in models:
            output, exec_time = run_single_test(model, user_input, idx)
            print_test_result(model, user_input, output, exec_time)

            # Store result for JSON export
            result_entry = {
                "model": model,
                "user_input": user_input,
                "output": output,
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
    for case_idx, user_input in enumerate(cases):
        for model_idx, model in enumerate(models):
            task_key = (case_idx, model_idx)  # 使用(case索引, model索引)作为任务的键
            tasks.append((model, user_input, idx, task_key))
            idx_map[task_key] = idx  # 保存任务键到原始索引的映射
            idx += 1
    
    # Use ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit tasks to executor
        future_to_task = {
            executor.submit(run_single_test_task, model, user_input, task_idx, result_lock, results, task_key): 
            (model, user_input, task_idx, task_key) 
            for model, user_input, task_idx, task_key in tasks
        }
        
        # Print results as they are completed
        for future in as_completed(future_to_task):
            model, user_input, output, exec_time, _ = future.result()
            print_test_result(model, user_input, output, exec_time)
    
    # Sort results by case index and model index
    sorted_results = sorted(results, key=lambda x: (x['case_idx'], x['model_idx']))
    
    # Delete case_idx and model_idx from results
    for result in sorted_results:
        del result['case_idx']
        del result['model_idx']
    
    # Save results to JSON file
    save_results_to_json(sorted_results)

def run_single_test_task(model, user_input, idx, result_lock, results, task_key):
    """Run a single test task in a thread and return the result"""
    output, exec_time = run_single_test(model, user_input, idx)
    
    # Store result for JSON export
    with result_lock:
        result_entry = {
            "model": model,
            "user_input": user_input,
            "output": output,
            "execution_time": exec_time,
            "case_idx": task_key[0],
            "model_idx": task_key[1]
        }
        results.append(result_entry)
    
    return model, user_input, output, exec_time, task_key


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
