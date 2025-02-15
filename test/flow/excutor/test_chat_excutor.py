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
            {
                "step": "step 1",
                "intent": "Find reliable news websites from Reuters, AP and other authoritative sources",
                "Description": "Search and identify the webpage URL for news retrieval, ensuring it's a reliable news source",
                "Reason": "To get the news from the web page."
            },
            {
                "step": "step 2", 
                "intent": "Extract and retrieve news content from the webpage",
                "Description": "Scrape news content from the identified webpage URL, including key information such as headlines, body text, and timestamps", 
                "Reason": "Obtain the latest news content to provide raw data for subsequent document generation"
            },
            {
                "step": "step 3",
                "intent": "Knowledge Documentation Generation and Upload", 
                "Description": "Utilize the tool that generates documentation and uploads to GitBook to compile all useful and meaningful knowledge produced during the plan's execution into a document and upload it to GitBook, ensuring long-term preservation and reuse of valuable information.",
                "Reason": "To document the the news and the process of the news to the GitBook"
            }
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
            # {'step': 'step 2', 'intent': 'Content Summarization', 'Description': 'Summarize the filtered news articles into concise and digestible formats using a natural language processing engine.', 'Reason': 'To provide the user with quick and easy-to-understand summaries of the news.'}
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

@pytest.mark.parametrize("plan,messages", [
    (
        [
            {
                'step': 'step 1', 
                'intent': 'Mysql Query', 
                'Description': 'Execute SQL query to retrieve data from database using specified parameters and conditions.',
                'Reason': 'To fetch accurate and relevant data from the MySQL database for further processing and analysis.',
            },
            {
                'step': 'step 2', 
                'intent': 'Content Summarization', 
                'Description': 'Summarize the filtered news articles into concise and digestible formats using a natural language processing engine.',
                'Reason': 'To provide the user with quick and easy-to-understand summaries of the news.'
            }
        ],
        [
            {"role": "user", "content": "search the latest news about AI"},
        ]
    )
])
def test_handle_new_tool_execution_no_suitable_tool_found(plan, messages):
    handle_new_tool_execution(plan, messages, "user_id")
    print("executed need input plan", plan)
    assert plan[0]["tool"] == "No tool found for current step"
