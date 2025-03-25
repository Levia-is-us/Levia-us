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

from engine.flow.episodic_memory_handle_flow.execute_episodic_memory_flow import process_tool_execution_plan
from engine.flow.episodic_memory_handle_flow.execute_episodic_memory_flow import episodic_memory_executor


@pytest.mark.parametrize("plan", [
    ([{
	'step': 'step 1',
	'tool': 'WebSearchTool',
	'data': {
		'method': 'web_search',
		'inputs': [{
			'name': 'intent',
			'type': 'str',
			'required': True,
			'description': "User's search intention or query context used to generate keywords",
			'source': 'context',
			'method': 'direct',
			'value': 'Hi Levia, can you tell me the latest advancements in quantum computing as of 2025?',
			'confidence': 'high'
		}],
		'output': {
			'description': "List of relevant URLs or 'No results found' message",
			'type': 'Union[List[str], str]'
		}
	},
	'step purpose': 'Retrieve URLs of news articles or updates',
	'description': 'Perform a web search to gather URLs of relevant news articles or updates.',
	'reason': 'This step is necessary to obtain the initial data (URLs) that will be used in the next step for content analysis.'
}, {
	'step': 'step 2',
	'tool': 'WebsiteScanTool',
	'data': {
		'method': 'website_scan',
		'inputs': [{
			'name': 'url_list',
			'type': 'list',
			'required': True,
			'description': 'Initial list of website URLs to begin scanning from'
		}, {
			'name': 'intent',
			'type': 'str',
			'required': True,
			'description': 'Guidance parameter to filter relevant content during scanning',
			'source': 'context',
			'method': 'direct',
			'value': 'Hi Levia, can you tell me the latest advancements in quantum computing as of 2025?',
			'confidence': 'high'
		}],
		'output': {
			'description': 'Processed summary of website content matching the specified intent',
			'type': 'list/dict (implementation-dependent)'
		}
	},
	'step purpose': 'Filter and summarize relevant content',
	'description': "Scan the retrieved URLs to filter and summarize the content based on the user's intent.",
	'reason': 'This step is necessary to analyze the content of the URLs and provide the user with relevant and summarized information.'
}]),
])
def test_process_tool_execution_plan(plan):
    chat_messages = [
        {"role": "user", "content": "search some news"},
    ]
    res = process_tool_execution_plan(plan, "user_id", chat_messages)
    print(res)


@pytest.mark.parametrize("chat_messages", [
    ([
        {"role": "user", "content": "search some news"},
    ]),
])
def test_episodic_memory_executor(chat_messages):
    episodic_memory_executor("user_id", 'User requests execution of a news search operation', chat_messages)
