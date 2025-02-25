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

from engine.flow.episodic_memory_handle_flow.episodic_check_prompt import episodic_check_prompt
from engine.llm_provider.llm import chat_completion
from engine.utils.json_util import extract_json_from_str
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def episodic_check(user_intent, context, plan, user_id):
    prompt = episodic_check_prompt(user_intent, context, plan)
    result = chat_completion(prompt, QUALITY_MODEL_NAME, config={"temperature": 0}, user_id=user_id)
    start_tag = "<think>"
    end_tag = "</think>"
    start_index = result.find(start_tag)
    end_index = result.find(end_tag)
    if start_index != -1 and end_index != -1 and end_index > start_index:
        result = result[:start_index] + result[end_index + len(end_tag):].replace('\n', '')
    try:
        result = extract_json_from_str(result)
    except:
        massage = "wrong format of episodic_check result: " + result
        raise Exception(massage)
    return result


if __name__ == "__main__":
    user_intent = "User requests retrieval of recent news updates across general topics"
    context = [{"role": "user", "content": "Hello,, I am Olive, I like football!"},
               {"role": "assistant", "content": """Hello Olive! It’s fantastic to connect with someone who loves football—it’s a sport that truly brings people together! ⚽ While I’m still learning the nuances of every league and player, I’d love to hear more about what excites you most. Do you follow a specific team, or is there a player whose skills leave you in awe?

As we chat, I'll keep refining my understanding of your preferences, so I can eventually share tailored insights or historical trivia you might enjoy. For instance, if you mention liking tactical gameplay, I could analyze patterns from iconic matches, or if you admire a particular striker, I might compare their stats across seasons. The more we talk football, the better I’ll get at being your personal sideline analyst! What sparks your passion for the game?"""},
               {"role": "user", "content": "can you tell me some news?"},
               ]

    plan = [
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
                        'description': "User's search intention or query context used to generate keywords",
                        'source': 'context',
                        'method': 'LLM'
                    }
                ],
                'output': {
                    'description': "List of relevant URLs or 'No results found' message",
                    'type': 'Union[List[str], str]'
                }
            },
            'step purpose': 'Perform a web search to find current news articles',
            'description': "Use the WebSearchTool to execute a web search based on the user's intent to find current news articles.",
            'reason': "This step is necessary to gather URLs of current news articles that match the user's search intent."
        },
        {
            'step': 'step 2', 
            'tool': 'WebsiteScanTool',
            'data': {
                'method': 'website_scan',
                'inputs': [
                    {
                        'name': 'url_list',
                        'type': 'list',
                        'required': True,
                        'description': 'Initial list of website URLs to begin scanning from',
                        'source': 'step 1',
                        'method': 'direct'
                    },
                    {
                        'name': 'intent',
                        'type': 'str',
                        'required': True,
                        'description': 'Guidance parameter to filter relevant content during scanning',
                        'source': 'context',
                        'method': 'LLM'
                    }
                ],
                'output': {
                    'description': 'Processed summary of website content matching the specified intent',
                    'type': 'list/dict (implementation-dependent)'
                }
            },
            'step purpose': 'Extract relevant content from the search results',
            'description': 'Use the WebsiteScanTool to scan the URLs obtained from the web search and extract relevant news content.',
            'reason': 'This step is necessary to filter and summarize the content from the search results to provide the user with relevant news articles.'
        }
    ]
    print(episodic_check(user_intent, context, plan))
