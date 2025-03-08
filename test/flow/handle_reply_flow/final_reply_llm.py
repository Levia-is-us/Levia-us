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

from engine.flow.handle_reply_flow.generate_reply_flow import handle_reply_flow
from engine.utils.json_util import extract_code_breakdown_from_doc, extract_str_from_doc

engine_output = plan_steps = [
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
                    'method': 'LLM',
                    'value': 'Latest news headlines for March 8, 2025 in the United States'
                }
            ],
            'output': {
                'description': 'List of relevant URLs matching the intent, or error message if no results found',
                'type': 'Union[List[str], str]'
            },
            'tool': 'WebSearchTool'
        },
        'step purpose': 'Retrieve current news URLs',
        'description': "Perform a web search using the intent 'Latest news headlines for March 8, 2025' to identify recent news articles from credible sources. This addresses the user's need for real-time information beyond the AI's knowledge cutoff.",
        'tool_executed_result': [
            'https://www.npr.org/sections/news/',
            'https://www.usnews.com/news',
            'https://www.cnn.com/2025/03/07/us/5-things-to-know-for-march-7/index.html'
        ],
        'executed': True
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
                    'description': 'List of initial URLs to start website scanning from',
                    'source': 'step 1',
                    'method': 'direct',
                    'value': ''
                },
                {
                    'name': 'intent',
                    'type': 'str',
                    'required': True,
                    'description': 'Guiding purpose for content filtering and summarization',
                    'source': 'context',
                    'method': 'LLM',
                    'value': 'Summarize key news developments from March 8, 2025 in the United States'
                }
            ],
            'output': {
                'description': 'Processed website content summary or timeout error message',
                'type': 'str'
            },
            'tool': 'WebsiteScanTool'
        },
        'step purpose': 'Extract news content',
        'description': "Scan the URLs obtained from Step 1 using the intent 'Summarize key news developments from March 8, 2025' to filter and condense information into a coherent news summary, handling potential timeouts or inaccessible sources.",
        'tool_executed_result': '<<ASSISTANT_CONVERSATION_START>>\n\n# U.S. News Overview: Major Headlines and Developments (2025/03/08)\n\n## Top Stories\n\n### Politics and Government\n- **Trump Administration Restructuring**: President Trump is expected to sign an executive order to dismantle the Department of Education. This move has raised concerns about the future of trillions of dollars in student loans.\n- **Federal Agency Changes**: Concerns are growing about Elon Musk\'s role in government restructuring, with mental health workers at the VA describing his "What did you do last week?" emails as "psychological warfare." President Trump has clarified that Cabinet secretaries, not Musk, are in charge of agency cuts.\n- **Trade Tensions**: The administration has delayed implementing tariffs on Canada and Mexico by almost a month. Five Democratic state treasurers have called for an end to the trade war, warning of detrimental impacts on Americans. Canadian Prime Minister Trudeau stated Canada "will not back down from a fight."\n\n### Economy\n- **Job Market**: February\'s employment report shows steady job growth, though analysts note Trump\'s federal worker firings may not appear in data for months. Many fired CDC workers, including Bri McNulty who shared her story with NPR, have been reinstated.\n- **Markets**: U.S. stocks have declined amid tariff uncertainty. The Nasdaq has fallen more than 7% and the S&P 500 is down more than 4% since Trump took office. Tesla shares have dropped around 40% from their December peak.\n- **Corporate News**: Walgreens has agreed to be acquired by a private equity firm for almost $10 billion, which would take the drugstore chain private after nearly 100 years as a publicly traded company.\n\n### Science and Technology\n- **SpaceX Setback**: SpaceX\'s Starship spacecraft exploded shortly after liftoff, marking the second failure in six weeks. The FAA temporarily halted flights into several Florida airports due to "falling space debris" and is requiring SpaceX to conduct a mishap investigation.\n- **Cryptocurrency**: President Trump has signed an order creating a cryptocurrency strategic reserve using seized bitcoin and is scheduled to speak with crypto founders and investors at a White House summit.\n\n### Health\n- **Measles Outbreak**: A measles outbreak in West Texas has grown to at least 159 cases and spread to New Mexico, with two confirmed deaths. The kindergarten vaccination rate in Gaines County is 82%, below the 95% needed for herd immunity.\n- **CDC Study**: The CDC is reportedly planning a study into vaccines and autism, according to sources cited by U.S. News.\n\n### International\n- **Ukraine Relations**: U.S. officials are working to mend ties with Ukraine following a contentious meeting between Presidents Trump and Zelensky. European leaders are proceeding with their own Ukraine peace summit plans.\n- **European Transport Disruption**: An unexploded WWII bomb discovered near Paris has halted Eurostar train travel between London and northern France.\n- **China Relations**: China\'s top foreign policy official addressed the escalating trade war with the U.S., characterizing Trump\'s policies as "two-faced" and promoting China as an "anchor" on the global stage.\n\n## Other Significant Developments\n- **Transgender Athletes**: California Governor Gavin Newsom broke with most Democrats by stating that transgender athletes playing in women\'s sports is "deeply unfair," aligning more closely with Trump\'s recent executive order on the issue.\n- **Arts Funding**: Arts groups are suing the National Endowment for the Arts over new grant restrictions related to "gender ideology" stemming from a recent Trump executive order.\n- **Climate Policy**: Ambassador André Aranha Corrêa do Lago will lead COP30 efforts on climate change as the U.S. reduces its international involvement.\n- **Daylight Saving Time**: Americans are preparing to move clocks forward one hour this Sunday for Daylight Saving Time.',
        'executed': True
    }
]

chat_messages = [
    {"role": "user", "content": "What is Bitcoin?"},
    {"role": "assistant", "content": engine_output},
]

final_reply = handle_reply_flow(chat_messages, [{"normal_llm_reply": engine_output}])

analysis = extract_code_breakdown_from_doc(final_reply)
final_reply = extract_str_from_doc(final_reply)