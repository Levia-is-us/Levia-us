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
from engine.flow.planner.make_tool_base_plan_flow import tool_base_planner


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


def run_single_test(model, test_case, idx):
    """Run a single test case and return the result"""
    os.environ["CHAT_MODEL_NAME"] = model
    intent = test_case["intent"]
    context = [{"role": "user", "content": test_case["input"]}]
    tool_list = [
        {
            "id": "web_search_tool-web_search",
            "metadata": {
                "data": '{"method": "web_search", "inputs": [{"name": "intent", '
                '"type": "str", "required": true, "description": '
                "\"User's search intention or query context used to "
                'generate keywords"}], "output": {"description": "List '
                "of relevant URLs or 'No results found' message\", "
                '"type": "Union[List[str], str]"}}',
                "description": "The code contains one main function exposed "
                "through the @run_tool decorator:\n"
                "\n"
                "1. web_search method in WebSearchTool class\n"
                "   - Signature: def web_search(self, intent: "
                "str)\n"
                "   - Parameters:\n"
                "     - intent (str, required): User's search "
                "intent\n"
                "   - Return: List[str] or str (based on code "
                "implementation)\n"
                "   - Purpose: Performs web search using "
                "generated keywords, handles visual/non-visual "
                "mode via environment variable\n"
                "   - Notable: Return type inconsistency between "
                "docstring (list) and code (list/str), "
                "environment dependency\n"
                "   - Edge cases: Empty results return strings "
                "instead of lists, VISUAL environment variable "
                "affects search method",
                "details": "Performs a web search using keywords generated from "
                "the user's intent. The search mode "
                "(visual/non-visual) is determined by the VISUAL "
                "environment variable. Returns a list of relevant "
                "URLs if found, otherwise returns a 'No results "
                "found' message. Handles both text-based and visual "
                "search implementations through external service "
                "calls.",
                "method": "web_search",
                "short_description": "Search web content based on user intent "
                "and retrieve relevant URLs",
                "timestamp": 1739523889095.0,
                "tool": "WebSearchTool",
                "uid": "levia",
            },
            "score": 0.266156107,
            "values": [],
        },
        {
            "id": "website_scan_tool-website_scan",
            "metadata": {
                "data": '{"method": "website_scan", "inputs": [{"name": '
                '"url_list", "type": "list", "required": true, '
                '"description": "Initial list of website URLs to begin '
                'scanning from"}, {"name": "intent", "type": "str", '
                '"required": true, "description": "Guidance parameter to '
                'filter relevant content during scanning"}], "output": '
                '{"description": "Processed summary of website content '
                'matching the specified intent", "type": "list/dict '
                '(implementation-dependent)"}}',
                "description": "1. Identified functions:\n"
                "   - website_scan (method of WebsiteScanTool "
                "class decorated via class-level @run_tool)\n"
                "\n"
                "2. Analysis of website_scan:\n"
                "   a. Function signature: \n"
                "      def website_scan(self, url_list: list, "
                "intent: str)\n"
                "   \n"
                "   b. Parameters:\n"
                "      - url_list: list (required), list of URLs "
                "to scan\n"
                "      - intent: str (required), guides scanning "
                "focus\n"
                "   \n"
                "   c. Return value: \n"
                "      - result (type not explicitly shown but "
                "implied to be processed content)\n"
                "      - Based on context, likely returns "
                "list/dict of summarized information\n"
                "   \n"
                "   d. Purpose:\n"
                "      - Orchestrates website scanning pipeline: "
                "link collection, deduplication, intent-based "
                "filtering, content extraction, and "
                "summarization\n"
                "   \n"
                "   e. Notable aspects:\n"
                "      - Relies on external utils functions "
                "(get_all_links, get_summary_links etc.)\n"
                "      - No visible error handling for network "
                "requests or invalid URLs\n"
                "      - Sequential processing with multiple data "
                "transformation steps\n"
                "   \n"
                "   f. Potential issues:\n"
                "      - No validation for URL format in "
                "url_list\n"
                "      - No timeout handling for get_all_content\n"
                "      - Dependency on external utils that aren't "
                "shown in code\n"
                "      - Return type depends on get_summary_links "
                "implementation",
                "details": "Processes a list of URLs by collecting all links, "
                "removing duplicates, filtering based on intent, "
                "extracting content, and generating summarized "
                "results. Implements a multi-stage pipeline for web "
                "content analysis.",
                "method": "website_scan",
                "short_description": "Scan websites and extract intent-relevant "
                "information",
                "timestamp": 1739523704208.0,
                "tool": "WebsiteScanTool",
                "uid": "levia",
            },
            "score": 0.207122058,
            "values": [],
        },
        {
            "id": "create_gitbook_tool-save_markdown_to_gitbook",
            "metadata": {
                "data": '{"method": "save_markdown_to_gitbook", "inputs": '
                '[{"name": "content", "type": "str", "required": true, '
                '"description": "Markdown/text content to be saved, '
                'required for article creation"}, {"name": '
                '"gitbook_api_key", "type": "str", "required": true, '
                '"description": "API key for GitBook authentication, '
                'obtained from environment configuration"}, {"name": '
                '"azure_file_server_key", "type": "str", "required": '
                'true, "description": "Credentials for Azure file '
                'storage service, used for temporary content hosting"}, '
                '{"name": "user_website_url", "type": "str", "required": '
                'true, "description": "Base URL prefix for the final '
                'published content location"}], "output": '
                '{"description": "Final published URL string on success, '
                'error message string on failure", "type": "str"}}',
                "description": "Identified function:\n"
                "- save_markdown_to_gitbook (method of "
                "SaveMarkdownToGitbook class decorated via "
                "@run_tool)\n"
                "\n"
                "Function signature:\n"
                "def save_markdown_to_gitbook(content, "
                "gitbook_api_key, azure_file_server_key, "
                "user_website_url)\n"
                "\n"
                "Parameters:\n"
                "1. content (no type hint) - required - "
                "markdown/text content to process\n"
                "2. gitbook_api_key (no type hint) - required - "
                "API key for GitBook access\n"
                "3. azure_file_server_key (no type hint) - "
                "required - Credentials for Azure file storage\n"
                "4. user_website_url (no type hint) - required - "
                "Base URL for constructed result\n"
                "\n"
                "Return value:\n"
                "- String containing final URL or error message "
                "(type: str)\n"
                "\n"
                "Purpose:\n"
                "Uploads markdown content to GitBook through a "
                "multi-step process involving Azure file storage "
                "upload, GitBook API interactions for content "
                "import, and change request management.\n"
                "\n"
                "Notable aspects:\n"
                "1. Uses global singleton instances for "
                "GitBookAPI and file_manage\n"
                "2. Implicit requirement for .env file "
                "configuration\n"
                "3. Relies on first organization/space from "
                "GitBook API responses\n"
                "4. Automatic cleanup of uploaded files on "
                "errors\n"
                "5. No explicit type validation for input "
                "parameters\n"
                "\n"
                "Edge cases/issues:\n"
                "- Fails if user has no organizations/spaces in "
                "GitBook\n"
                "- Potential race conditions with global "
                "_gitbook/_file_manage\n"
                "- Assumes first item in organizations/spaces "
                "lists is correct\n"
                "- No retry mechanism for API calls\n"
                "- Return type inconsistency (URL string vs error "
                "message string)",
                "details": "Processes markdown content by uploading to Azure "
                "storage, importing to GitBook through API calls, "
                "managing change requests, and returning the final "
                "URL. Handles error cleanup and API interactions with "
                "GitBook's organization/space structure.",
                "method": "save_markdown_to_gitbook",
                "short_description": "Save markdown content to GitBook via API "
                "integration",
                "timestamp": 1739522626491.0,
                "tool": "SaveMarkdownToGitbook",
                "uid": "levia",
            },
            "score": 0.183254138,
            "values": [],
        },
        {
            "id": "list_abilities_tool-list_abilities",
            "metadata": {
                "data": '{"method": "list_abilities", "inputs": [{"name": '
                '"kwargs", "type": "dict", "required": false, '
                '"description": "Optional keyword arguments (not '
                'explicitly used in current implementation)"}], '
                '"output": {"description": "Dictionary mapping method '
                'names to their metadata (description and signature)", '
                '"type": "dict"}}',
                "description": "The analysis focuses on the ListAbilitiesTool "
                "class and its list_abilities method:\n"
                "\n"
                "1. Identified Function:\n"
                "   - list_abilities (method of ListAbilitiesTool "
                "class decorated via @run_tool class decorator)\n"
                "\n"
                "2. Function Signature Analysis:\n"
                "   - Signature: def list_abilities(self, "
                "**kwargs) -> dict\n"
                "   - Parameters:\n"
                "     - self: Implicit class instance reference "
                "(required)\n"
                "     - **kwargs: Variable keyword arguments "
                "(optional)\n"
                "   - Return Type: dict\n"
                "\n"
                "3. Implementation Notes:\n"
                "   - Relies on self.methods inherited from "
                "BaseTool (not shown in code)\n"
                "   - Uses introspection to get method "
                "signatures\n"
                "   - Contains error handling for signature "
                "extraction failures\n"
                "   - Returns structured ability metadata "
                "including descriptions and signatures\n"
                "\n"
                "4. Potential Issues:\n"
                "   - Dependent on parent class implementation "
                "(self.methods and self.get_method_description)\n"
                "   - **kwargs parameters are declared but not "
                "used in implementation\n"
                "   - Signature detection might fail for "
                "non-standard methods (e.g., @classmethod)",
                "details": "Collects metadata about all registered tool methods "
                "including their descriptions and method signatures. "
                "Iterates through registered methods, attempts to "
                "extract parameter information via code "
                "introspection, and returns structured data for API "
                "discovery purposes.",
                "method": "list_abilities",
                "short_description": "List available abilities with descriptions "
                "and signatures",
                "timestamp": 1739522797152.0,
                "tool": "ListAbilitiesTool",
                "uid": "levia",
            },
            "score": 0.105819918,
            "values": [],
        },
    ]

    start = int(time.time())
    try:
        output = tool_base_planner(
            intent, tool_list, f"user-{idx}", f"ch-{idx}", context
        )
    except Exception as e:
        output = f"Error in model [{model}] for input [{test_case['input']}: {str(e)}"
    end = int(time.time())
    return output, round((end - start), 2)


def print_test_result(model, content, intent, output, exec_time):
    """Format and print test result"""

    print(f"{'-'*100}")
    print(f"🤖  Model: {model}")
    print(f"📝  Input: {content}")
    print(f"📝  Intent: {intent}")
    print(f"📊  Output: {output}")
    print(f"⏱️  Execution time: {exec_time} seconds")


def calculate_model_statistics(results):
    """Calculate statistics for each model's execution times"""
    model_stats = {}

    for model in models:
        model_times = [r["execution_time"] for r in results if r["model"] == model]
        if model_times:
            model_stats[model] = {
                "avg_time": round(sum(model_times) / len(model_times), 2),
                "min_time": min(model_times),
                "max_time": max(model_times),
                "total_cases": len(model_times),
            }

    print("\n" + "-" * 100)
    print("Model Performance Statistics:")
    for model, stats in model_stats.items():
        print(f"\nModel: {model}")
        print(f"Average Time: {stats['avg_time']} seconds")
        print(f"Minimum Time: {stats['min_time']:.2f} seconds")
        print(f"Maximum Time: {stats['max_time']:.2f} seconds")
        print(f"Total Test Cases: {stats['total_cases']}")
        print("\n" + "-" * 100)

    return model_stats


def save_results_to_json(results):
    """Save test results and statistics to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Calculate statistics
    model_stats = calculate_model_statistics(results)

    # Group results by model
    results = {model: [r for r in results if r["model"] == model] for model in models}

    # Combine results and stats
    final_results = {
        "model_statistics": model_stats,
        "test_results": results,
    }

    save_path = Path(__file__).parent / f"toolbase_planner_test_results_{timestamp}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to: {save_path}")


def linear_execute(cases: list):
    """Linearly execute test cases"""
    idx = 1
    results = []

    # For each test case, test with all models
    for test_case in cases:
        for model in models:
            output, exec_time = run_single_test(model, test_case, idx)
            # Print test result
            print_test_result(
                model, test_case["input"], test_case["intent"], output, exec_time
            )

            # Store result for JSON export
            result_entry = {
                "model": model,
                "user_input": test_case["input"],
                "intent": test_case["intent"],
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
            model, input, intent, output, exec_time, _ = future.result()
            print_test_result(model, input, intent, output, exec_time)

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
    intent = test_case["intent"]
    user_input = test_case["input"]

    # Store result for JSON export
    with result_lock:
        result_entry = {
            "model": model,
            "user_input": user_input,
            "intent": intent,
            "output": output,
            "execution_time": exec_time,
            "case_idx": task_key[0],
            "model_idx": task_key[1],
        }
        results.append(result_entry)
    return model, user_input, intent, output, exec_time, task_key


def test_tool_base_planner_llm(is_concurrent=True):
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
    test_tool_base_planner_llm()
