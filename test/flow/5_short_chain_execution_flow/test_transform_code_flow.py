import os
import sys
import dotenv

current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
)
# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from engine.flow.executor.get_transform_code_flow import transform_code


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
        'step purpose': 'Retrieve current news URLs',
        'description': 'Use web search to find recent news articles and official sources about China from March 8, 2025. This addresses the core need to identify timely, relevant news sources through keyword generation and URL extraction based on the specified intent.',
        'tool_executed_result': {'url_list': ['https://www.china-briefing.com/news/chinas-two-sessions-2025-takeaways-government-work-report/', 'https://apnews.com/article/china-taiwan-japan-foreign-affairs-8261e3583defaea2df3f0d602f6bd9c8', 'https://www.reuters.com/markets/asia/chinas-imports-tumble-demand-skids-trade-war-heats-up-2025-03-07/']},
        'executed': True
    },
    {
        'step': 'step 2', 
        'tool': 'WebsiteScanTool',
        'data': '{"method": "website_scan", "inputs": [{"name": "url_list", "type": "list", "required": true, "description": "List of initial URLs to start website scanning from"}, {"name": "intent", "type": "str", "required": true, "description": "Guiding purpose for content filtering and summarization"}], "output": {"description": "Processed website content summary or timeout error message", "type": "str"}}',
        'step purpose': 'Analyze news content',
        'description': "Scan identified URLs to extract and summarize key China-related news stories, filtering content based on the user's intent for 'latest news'. This handles content aggregation, duplicate removal, and intent-focused summarization from potentially complex website structures."
    }
]

next_step_reply = {
    'step': 'step 2',
    'can_proceed': True,
    'extracted_arguments': {
        'required_arguments': {
            'url_list': {
                'source': 'step 1',
                'method': 'code',
                'value': [
                    'https://www.china-briefing.com/news/chinas-two-sessions-2025-takeaways-government-work-report/',
                    'https://apnews.com/article/china-taiwan-japan-foreign-affairs-8261e3583defaea2df3f0d602f6bd9c8',
                    'https://www.reuters.com/markets/asia/chinas-imports-tumble-demand-skids-trade-war-heats-up-2025-03-07/'
                ]
            },
            'intent': {
                'source': 'context',
                'method': 'LLM',
                'value': 'Retrieve and summarize the latest news in China from March 8, 2025, focusing on key developments and official sources'
            }
        }
    }
}

if __name__ == "__main__":
    result = transform_code(plan_steps,next_step_reply, "user_id", "ch_id")
    print(result)
