import os
import sys
import dotenv
import pytest

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
print(project_root)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)

from engine.flow.executor.chat_executor import handle_new_tool_execution

@pytest.mark.parametrize("plan,messages", [
    (
        [
            {'step': 'step 1', 'intent': 'Data Extraction', 'Description': 'Retrieve the latest news articles from reliable sources using a web scraping or API tool.', 'Reason': 'To gather up-to-date and relevant news content for the user.'},
            {'step': 'step 2', 'intent': 'Content Summarization', 'Description': 'Summarize the filtered news articles into concise and digestible formats using a natural language processing engine.', 'Reason': 'To provide the user with quick and easy-to-understand summaries of the news.'}
        ],
        [
            {"role": "user", "content": "search the latest news about AI"},
        ]
    )
])
def test_handle_new_tool_execution(plan, messages):
    handle_new_tool_execution(plan, messages, "user_id")
    print("executed plan", plan)

test_data = [
    (
        [
            {'step': 'step 1', 'intent': 'Data Extraction', 'Description': 'Retrieve the latest news articles from reliable sources using a web scraping or API tool.', 'Reason': 'To gather up-to-date and relevant news content for the user.'},
            {'step': 'step 2', 'intent': 'Content Summarization', 'Description': 'Summarize the filtered news articles into concise and digestible formats using a natural language processing engine.', 'Reason': 'To provide the user with quick and easy-to-understand summaries of the news.'}
        ],
        [
            {"role": "user", "content": "hello"},
        ]
    )
]

@pytest.mark.parametrize("plan,messages", test_data)
def test_terminal_handle_new_tool_execution_need_input(plan, messages):
    handle_new_tool_execution(plan, messages, "user_id")
    print("executed need input plan", plan)

@pytest.mark.parametrize("plan,messages", test_data)
def test_event_handle_new_tool_execution_need_input(monkeypatch, plan, messages):
    env_vars = dict(os.environ)
    env_vars["INTERACTION_MODE"] = "event"
    monkeypatch.setattr(os, "environ", env_vars)
    handle_new_tool_execution(plan, messages, "user_id")
    print("executed need input plan", plan)
    messages.append({"role": "user", "content": "I want to search the latest news about AI"})
    handle_new_tool_execution(plan, messages, "user_id")
    print("executed input plan", plan)
