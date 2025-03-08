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

from engine.flow.episodic_memory_handle_flow.check_episodic_flow import episodic_check



if __name__ == "__main__":
    user_intent = "The user wants to know the current news headlines and stories from the United States as of March 7, 2025."
    context = [
        {"role": "user", "content": "tell me the news today in USA"}
               ]

    plan = '[{\'step\': \'step 1\', \'tool\': \'WebSearchTool\', \'data\': {\'method\': \'web_search\', \'inputs\': [{\'name\': \'intent\', \'type\': \'str\', \'required\': True, \'description\': "User\'s search purpose or information need that drives the web search", \'source\': \'context\', \'method\': \'LLM\'}], \'output\': {\'description\': \'List of relevant URLs matching the intent, or error message if no results found\', \'type\': \'Union[List[str], str]\'}}, \'step purpose\': \'Retrieve current news URLs\', \'description\': "Perform a web search using the intent \'Latest news headlines for March 4, 2025\' to identify recent news articles from credible sources. This addresses the user\'s need for real-time information beyond the AI\'s knowledge cutoff."}, {\'step\': \'step 2\', \'tool\': \'WebsiteScanTool\', \'data\': {\'method\': \'website_scan\', \'inputs\': [{\'name\': \'url_list\', \'type\': \'list\', \'required\': True, \'description\': \'List of initial URLs to start website scanning from\', \'source\': \'step 1\', \'method\': \'direct\'}, {\'name\': \'intent\', \'type\': \'str\', \'required\': True, \'description\': \'Guiding purpose for content filtering and summarization\', \'source\': \'context\', \'method\': \'LLM\'}], \'output\': {\'description\': \'Processed website content summary or timeout error message\', \'type\': \'str\'}}, \'step purpose\': \'Extract news content\', \'description\': "Scan the URLs obtained from Step 1 using the intent \'Summarize key news developments from March 4, 2025\' to filter and condense information into a coherent news summary, handling potential timeouts or inaccessible sources."}]'
    
    print(episodic_check(user_intent, context, plan, "user_id", "ch_id"))
