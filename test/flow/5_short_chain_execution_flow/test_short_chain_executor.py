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

from engine.flow.executor.execute_short_chain_flow import process_tool_execution_plan
from engine.flow.executor.execute_short_chain_flow import process_plan_execution

@pytest.mark.parametrize("plan,messages", [
    (
        [
            {
                'step': 'step 1',
                'tool': 'WebSearchTool', 
                'data': '{"method": "web_search", "inputs": [{"name": "intent", "type": "str", "required": true, "description": "User\'s search purpose or information need that drives the web search"}], "output": {"description": "List of relevant URLs matching the intent, or error message if no results found", "type": "Union[List[str], str]"}}',
                'step purpose': 'Find current news URLs',
                'description': "Perform a web search using the intent 'Latest global news for March 5, 2025' to retrieve fresh article URLs from reputable news sources, leveraging the tool's ability to generate search keywords from temporal context."
            },
            {
                'step': 'step 2',
                'tool': 'WebsiteScanTool',
                'data': '{"method": "website_scan", "inputs": [{"name": "url_list", "type": "list", "required": true, "description": "List of initial URLs to start website scanning from"}, {"name": "intent", "type": "str", "required": true, "description": "Guiding purpose for content filtering and summarization"}], "output": {"description": "Processed website content summary or timeout error message", "type": "str"}}',
                'step purpose': 'Extract news content', 
                'description': "Scan the URLs obtained from Step 1 using the intent 'Summarize key news events from March 5, 2025' to filter and process content, handling potential timeouts while extracting relevant information through recursive link analysis."
            }
        ],
        [
            {
                "role": "user",
                "content": "Tell me the news today"
            }
        ]
    )
])
def test_handle_new_tool_execution(plan, messages):
    process_tool_execution_plan(plan, messages, "user_id")
    print("executed plan", plan)

test_data =  [
    (
        [
            {
                'step': 'step 1',
                'tool': 'WebSearchTool', 
                'data': '{"method": "web_search", "inputs": [{"name": "intent", "type": "str", "required": true, "description": "User\'s search purpose or information need that drives the web search"}], "output": {"description": "List of relevant URLs matching the intent, or error message if no results found", "type": "Union[List[str], str]"}}',
                'step purpose': 'Find current news URLs',
                'description': "Perform a web search using the intent 'Latest global news for March 5, 2025' to retrieve fresh article URLs from reputable news sources, leveraging the tool's ability to generate search keywords from temporal context."
            },
            {
                'step': 'step 2',
                'tool': 'WebsiteScanTool',
                'data': '{"method": "website_scan", "inputs": [{"name": "url_list", "type": "list", "required": true, "description": "List of initial URLs to start website scanning from"}, {"name": "intent", "type": "str", "required": true, "description": "Guiding purpose for content filtering and summarization"}], "output": {"description": "Processed website content summary or timeout error message", "type": "str"}}',
                'step purpose': 'Extract news content', 
                'description': "Scan the URLs obtained from Step 1 using the intent 'Summarize key news events from March 5, 2025' to filter and process content, handling potential timeouts while extracting relevant information through recursive link analysis."
            }
        ],
        [
            {
                "role": "user",
                "content": "Tell me the news today"
            }
        ]
    )
]

@pytest.mark.parametrize("plan,messages", test_data)
def test_terminal_handle_new_tool_execution_need_input(plan, messages):
    process_tool_execution_plan(plan, messages, "user_id")
    print("executed need input plan", plan)

@pytest.mark.parametrize("plan,messages", test_data)
def test_event_handle_new_tool_execution_need_input(monkeypatch, plan, messages):
    process_tool_execution_plan(plan, messages, "user_id")
    print("executed need input plan", plan)
    messages.append({"role": "user", "content": "I want to search the latest news about AI"})
    process_tool_execution_plan(plan, messages, "user_id")
    print("executed input plan", plan)

@pytest.mark.parametrize("plan,messages", [
    (
        [
            {
                'step': 'step 1',
                'tool': 'WebSearchTool', 
                'data': '{"method": "web_search", "inputs": [{"name": "intent", "type": "str", "required": true, "description": "User\'s search purpose or information need that drives the web search"}], "output": {"description": "List of relevant URLs matching the intent, or error message if no results found", "type": "Union[List[str], str]"}}',
                'step purpose': 'Find current news URLs',
                'description': "Perform a web search using the intent 'Latest global news for March 5, 2025' to retrieve fresh article URLs from reputable news sources, leveraging the tool's ability to generate search keywords from temporal context."
            },
            {
                'step': 'step 2',
                'tool': 'WebsiteScanTool',
                'data': '{"method": "website_scan", "inputs": [{"name": "url_list", "type": "list", "required": true, "description": "List of initial URLs to start website scanning from"}, {"name": "intent", "type": "str", "required": true, "description": "Guiding purpose for content filtering and summarization"}], "output": {"description": "Processed website content summary or timeout error message", "type": "str"}}',
                'step purpose': 'Extract news content', 
                'description': "Scan the URLs obtained from Step 1 using the intent 'Summarize key news events from March 5, 2025' to filter and process content, handling potential timeouts while extracting relevant information through recursive link analysis."
            }
        ],
        [
            {
                "role": "user",
                "content": "Tell me the news today"
            }
        ]
    )
])
def test_handle_new_tool_execution_no_suitable_tool_found(plan, messages):
    process_tool_execution_plan(plan, messages, "user_id")
    print("executed need input plan", plan)
    assert plan[0]["tool"] == "No tool found for current step"

@pytest.mark.parametrize("plan,messages", [
    (
        [
            {
                'step': 'step 1',
                'tool': 'WebSearchTool', 
                'data': '{"method": "web_search", "inputs": [{"name": "intent", "type": "str", "required": true, "description": "User\'s search purpose or information need that drives the web search"}], "output": {"description": "List of relevant URLs matching the intent, or error message if no results found", "type": "Union[List[str], str]"}}',
                'step purpose': 'Find current news URLs',
                'description': "Perform a web search using the intent 'Latest global news for March 5, 2025' to retrieve fresh article URLs from reputable news sources, leveraging the tool's ability to generate search keywords from temporal context."
            },
            {
                'step': 'step 2',
                'tool': 'WebsiteScanTool',
                'data': '{"method": "website_scan", "inputs": [{"name": "url_list", "type": "list", "required": true, "description": "List of initial URLs to start website scanning from"}, {"name": "intent", "type": "str", "required": true, "description": "Guiding purpose for content filtering and summarization"}], "output": {"description": "Processed website content summary or timeout error message", "type": "str"}}',
                'step purpose': 'Extract news content', 
                'description': "Scan the URLs obtained from Step 1 using the intent 'Summarize key news events from March 5, 2025' to filter and process content, handling potential timeouts while extracting relevant information through recursive link analysis."
            }
        ],
        [
            {
                "role": "user",
                "content": "Tell me the news today"
            }
        ]
    )
])
def test_process_plan_execution(messages,plan):
    process_plan_execution(messages,plan['plan'],intent='the latest news', user_id='user_id', ch_id='ch_id')
    print("executed plan", plan)