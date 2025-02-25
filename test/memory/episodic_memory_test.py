import os
import sys
import dotenv
import pytest

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from memory.episodic_memory.episodic_memory import (
    store_long_pass_memory,
    delete_long_pass_memory,
)

# store_short_pass_memory("test", "test", {"test": "test"}, namespace="test")
# store_short_pass_memory("test2", "test2", {"test": "test2"}, namespace="test")

# memories = retrieve_short_pass_memory("test", namespace="test")

# memories = retrieve_short_pass_memory("location tool")
# print(memories)

@pytest.mark.parametrize("metadata", [
    ({
	"excution_record": [{
		'step': 'step 1',
		'tool': 'WebSearchTool',
		'data': {
			'method': 'web_search',
			'inputs': [],
			'output': {}
		},
		'step purpose': 'Search for news articles updated within the last 24 hours',
		'description': "Use the web search tool to find relevant news articles based on the user's intent.",
		'reason': 'This step requires an external tool to perform a web search and retrieve URLs of news articles.',
		'tool_executed_result': ['https://www.nbcnews.com/politics/meet-the-press/last-24-hours-have-been-news-overload-more-come-n1272883', 'https://www.cbsnews.com/'],
		'executed': True
	}, {
		'step': 'step 2',
		'tool': 'WebsiteScanTool',
		'data': {
			'method': 'website_scan',
			'inputs': [],
			'output': {}
		},
		'step purpose': 'Extract and summarize the content of the found articles',
		'description': 'Use the website scan tool to extract and summarize the content of the news articles found in step 1.',
		'reason': 'This step requires an external tool to process the URLs and generate a summary of the news content.',
		'tool_executed_result': '### Title: News Report (2025/02/17)\n**Summary:**  \nThe provided content from NBC News and CBS News highlights a series of significant political, national, and international events that have unfolded over the past 24 hours, with implications for the future. Here’s a detailed breakdown:\n\n1. **Political Developments in the U.S.:**  \n   - The House of Representatives voted to establish a select committee to investigate the January 6th Capitol attack, with two GOP members joining Democrats in support.  \n   - The Trump Organization’s CFO, Allen Weisselberg, surrendered to the Manhattan District Attorney’s office following a grand jury indictment, raising questions about the political implications of the Trump Organization’s business practices.  \n   - President Biden traveled to Surfside, Florida, to meet with first responders and families affected by the recent condo collapse, while Florida Governor Ron DeSantis reportedly asked former President Trump to postpone a rally near the tragedy.  \n   - The U.S. Supreme Court is set to deliver its final opinions for the term, including a closely watched voting-rights case.  \n\n2. **National News:**  \n   - New York City released additional results from its chaotic Democratic mayoral primary, which remains incomplete.  \n   - Former Defense Secretary Donald Rumsfeld passed away, and Bill Cosby was released from prison.  \n   - A third Oath Keeper pled guilty to charges related to the January 6th Capitol riot.  \n\n3. **International and Global Events:**  \n   - China criticized the U.S. for altering its wording on Taiwan policy, warning that it risks peace in the region.  \n   - Pope Francis remained hospitalized due to a “complex clinical picture,” extending his stay beyond initial expectations.  \n   - A measles outbreak in Texas raised public health concerns, while the U.S. continued to grapple with the ongoing COVID-19 pandemic, with over 33.8 million confirmed cases and 608,138 deaths reported.  \n\n4. **Economic and Policy Discussions:**  \n   - Democrats face challenges in the upcoming midterms, with Republicans holding a 12-point advantage on economic trust. President Biden’s approval ratings on the economy remain higher than those of congressional Democrats, prompting calls for candidates to align closely with his agenda.  \n   - The Trump administration’s firings of federal workers, including FAA employees, sparked legal challenges and public outcry, with debates over presidential power and whistleblower protections.  \n\n5. **Other Notable Stories:**  \n   - A new Florida law aimed at punishing social media companies for deplatforming political candidates was temporarily blocked by a judge.  \n   - The Surfside condo collapse death toll rose to 18, with 145 people still unaccounted for.  \n   - A CBS News report highlighted the ongoing crisis in the Middle East, including Hamas’ release of hostages and U.S. Secretary of State Marco Rubio’s discussions on Gaza.  \n\n**Key Takeaways:**  \nThe past 24 hours have been marked by a whirlwind of political, national, and international news, with significant implications for the 2022 and 2024 elections. Key issues include the January 6th investigation, the Trump Organization’s legal troubles, and the Biden administration’s response to crises like the Surfside collapse. Internationally, tensions over Taiwan and the Pope’s health have drawn attention, while domestic challenges such as the measles outbreak and federal firings continue to shape the national conversation.',
		'executed': True
        }
    ]
})
])
def test_store_long_pass_memory(metadata):
    store_long_pass_memory(id='search news', memory='search news', metadata=metadata)
    
def test_delete_long_pass_memory():
	delete_long_pass_memory('557491df-709d-4572-932f-d5ab39801470')
