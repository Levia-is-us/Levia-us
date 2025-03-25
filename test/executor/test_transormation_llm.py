import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.flow.executor.get_transform_code_flow import transform_code


if __name__ == "__main__":
    next_step_reply = {
        'step': 'step 2',
        'can_proceed': True,
        'extracted_arguments': {
            'required_arguments': {
                'url_list': {
                    'source': 'step 1',
                    'method': 'code',
                    'value': ['https://english.elpais.com/archive/2025-03-03/']
                },
                'intent': {
                    'source': 'context',
                    'method': 'LLM',
                    'value': 'latest news updates'
                }
            }
        }
    }

    plan_steps = [
        {
            'step': 'step 1',
            'tool': 'WebSearchTool',
            'data': {
                'method': 'web_search',
                'inputs': [
                    {
                        'name': 'intent',
                        'type': 'str',
                        'required': True,
                        'description': "User's search purpose or information need that drives the web search",
                        'source': 'context',
                        'method': 'LLM'
                    }
                ],
                'output': {
                    'description': 'List of relevant URLs matching the intent, or error message if no results found',
                    'type': 'Union[List[str], str]'
                }
            },
            'step purpose': 'Identify news sources',
            'description': "Use web_search to find URLs of news articles matching the user's intent for 'today's news (2025/03/03)'. The tool will generate search keywords from the intent and return relevant news URLs.",
            'tool_executed_result': [{'url': 'https://english.elpais.com/archive/2025-03-03/', 'description': 'El Pais'}],
            'executed': True
        },
        {
            'step': 'step 2',
            'tool': 'WebsiteScanTool',
            'data': '{"method": "website_scan", "inputs": [{"name": "url_list", "type": "list", "required": true, "description": "List of initial URLs to start website scanning from"}, {"name": "intent", "type": "str", "required": true, "description": "Guiding purpose for content filtering and summarization"}], "output": {"description": "Processed website content summary or timeout error message", "type": "str"}}',
            'step purpose': 'Extract news content',
            'description': "Use website_scan to process the URLs from step 1, recursively scan articles, and generate a summary filtered by the intent 'latest news updates'. This handles content extraction and time-sensitive filtering."
        }
    ]
    reply = transform_code(plan_steps, next_step_reply, "Local_Dev", "")
    print(reply)

