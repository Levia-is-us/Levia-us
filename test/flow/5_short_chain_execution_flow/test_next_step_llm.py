import sys
import os
# Get absolute path of current file
current_file_path = os.path.abspath(__file__)

# Get project root path (3 levels up)
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
)
# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from engine.flow.executor.execute_short_chain_flow import validate_tool_parameters


tool_config = {'method': 'website_scan', 'inputs': [{'name': 'url_list', 'type': 'list', 'required': True, 'description': 'List of initial URLs to start website scanning from'}, {'name': 'intent', 'type': 'str', 'required': True, 'description': 'Guiding purpose for content filtering and summarization'}], 'output': {'description': 'Processed website content summary or timeout error message', 'type': 'str'}, 'tool': 'WebsiteScanTool'}

messages_history = [
    {"role": "user", "content": "I want to search for the latest news updates"}
]

plan_steps = [
        {
            'step': 'step 1',
            'tool': 'WebSearchTool', 
            'data': '{"method": "web_search", "inputs": [{"name": "intent", "type": "str", "required": true, "description": "User\'s search purpose or information need that drives the web search"}], "output": {"description": "List of relevant URLs matching the intent, or error message if no results found", "type": "Union[List[str], str]"}}',
            'step purpose': 'Retrieve current news URLs',
            'description': "Perform a web search to identify authoritative news sources reporting US headlines as of March 7, 2025. This will use the web_search method with the intent 'Current US news headlines and major stories from March 7, 2025' to obtain relevant news article URLs."
        },
        {
            'step': 'step 2',
            'tool': 'WebsiteScanTool',
            'data': '{"method": "website_scan", "inputs": [{"name": "url_list", "type": "list", "required": true, "description": "List of initial URLs to start website scanning from"}, {"name": "intent", "type": "str", "required": true, "description": "Guiding purpose for content filtering and summarization"}], "output": {"description": "Processed website content summary or timeout error message", "type": "str"}}',
            'step purpose': 'Extract and summarize news content', 
            'description': "Scan the obtained news URLs to extract key article content, filter for relevance to current US news, and generate a consolidated summary. Uses the website_scan method with the intent 'Summarize latest US news headlines and story details from March 7, 2025' to ensure focus on timely information."
        }
    ]

if __name__ == "__main__":
    validate_tool_parameters(tool_config, messages_history, plan_steps, "user_id", "ch_id")

