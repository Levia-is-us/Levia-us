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

from engine.flow.executor.episodic_memory_executor import process_tool_execution_plan


@pytest.mark.parametrize("plan", [
    ([{
        'step': 'step 1',
        'intent': 'Data Extraction',
        'Description': 'Retrieve the latest news articles from reliable sources using a web scraping or API tool.',
        'Reason': 'To gather up-to-date and relevant news content for the user.',
        'tool': {
                'id': 'web_search_tool-web_search',
                'metadata': {
                        'data': '{"method": "web_search", "inputs": [{"name": "intent", '
                        '"type": "str", "required": true, "description": '
                        '"User\'s search intention or query context used to '
                        'generate keywords","source": ["context"], "method_parameter": "LLM", "type": "str;dict;list","value":"abc"}], "output": {"description": "List '
                        'of relevant URLs or \'No results found\' message", '
                        '"type": "Union[List[str], str]"}}',
                        'details': 'Performs a web search using keywords generated from '
                        "the user's intent. The search mode "
                        '(visual/non-visual) is determined by the VISUAL '
                        'environment variable. Returns a list of relevant '
                        "URLs if found, otherwise returns a 'No results "
                        "found' message. Handles both text-based and visual "
                        'search implementations through external service '
                        'calls.',
                        'method': 'web_search',
                        'short_description': 'Search web content based on user intent '
                        'and retrieve relevant URLs',
                        'timestamp': 1739523889095.0,
                        'tool': 'WebSearchTool',
                        'uid': 'levia',
                        'output': ['output_1', 'output_2']
                },
                'score': 0.335994571,
                'values': []
            }
        },{
                'step': 'step 2',
                'intent': 'Data Extraction',
                'Description': 'Retrieve the latest news articles from reliable sources using a web scraping or API tool.',
                'Reason': 'To gather up-to-date and relevant news content for the user.',
                'tool': {
                        'id': 'web_search_tool-web_search',
                        'metadata': {
                                'data': '{"method": "web_search", "inputs": [{"name": "intent", "type": "str", "required": true, "description": "User\'s search intention or query context used to generate keywords","source": ["output_1"], "method_parameter": "def convert_to_uppercase(text): return text.upper()", "type": "str;dict;list"}], "output": {"description": "List '
                                'of relevant URLs or \'No results found\' message", '
                                '"type": "Union[List[str], str]"}}',
                                'details': 'Performs a web search using keywords generated from '
                                "the user's intent. The search mode "
                                '(visual/non-visual) is determined by the VISUAL '
                                'environment variable. Returns a list of relevant '
                                "URLs if found, otherwise returns a 'No results "
                                "found' message. Handles both text-based and visual "
                                'search implementations through external service '
                                'calls.',
                                'method': 'web_search',
                                'short_description': 'Search web content based on user intent '
                                'and retrieve relevant URLs',
                                'timestamp': 1739523889095.0,
                                'tool': 'WebSearchTool',
                                'uid': 'levia',
                                'output': ['urls']
                        },
                        'score': 0.335994571,
                        'values': []
                }
        }]),
])
def test_process_tool_execution_plan(plan):
    process_tool_execution_plan(plan, "user_id")