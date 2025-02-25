import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework import run_tool, BaseTool

from tools.website_scan_tool.utils import (
    get_all_content,
    get_all_links,
    remove_duplicate_links,
    get_prompt_links,
    get_summary_links,
)



@run_tool("Website Scan Tool")
class WebsiteScanTool(BaseTool):
    """Tool for scanning website content"""
    
    def website_scan(self, url_list: list, intent: str):
        """
        Scan websites and extract relevant information
        Args:
            url_list: List of URLs and their summaries to scan
            intent: The intent to guide the scanning
        Returns:
            Extracted information
        """
        try:
            raw_links = get_all_links(url_list)
            unique_links = remove_duplicate_links(raw_links)
            links_with_content = get_all_content(unique_links)
            summary = get_summary_links(links_with_content, intent)
            return summary
        except Exception as e:
            if(str(e) == "website connection timeout"):
                return "website connection timeout"
            else:
                raise Exception(e)
            


user_prompt = """
You are Levia, an AI strategist specializing in creating engaging social media content. Your task is to transform detailed information into concise, interesting tweets that sound human-written. 

Here is the context of the user's query:
<context>
{context}
</context>

And here's the detailed information to summarize:
<engine_output>
{ENGINE_OUTPUT}
</engine_output>

Please follow these steps to create an engaging tweet:

1. Analyze the input and plan your tweet:
   Wrap your tweet planning process inside <tweet_planning> tags. Consider:
   - The main topic and its importance
   - The emotional tone (positive, negative, or neutral)
   - How to make the tweet concise, interesting, and human-like
   - If it's about cryptocurrencies or financial topics, maintain a positive, optimistic tone
   - Identify key phrases from the input that will be useful for the tweet
   - Brainstorm multiple tweet ideas (at least 3) before settling on the final one
   - Consider the target audience and how to make the tweet appealing to them
   - Ensure that no hashtags are included in the final tweet
   - Explicitly state which tweet idea you've chosen and why

2. Apply Twitter-style language:
   - Use casual, conversational language
   - Include common abbreviations and contractions
   - Add 1-2 relevant emojis to enhance the message
   - Use confident language, avoiding hedging words like "maybe" or "possibly"

3. Ensure conciseness:
   - Limit your tweet to a maximum of 200 characters
   - Focus on one key idea or message
   - Use punchy, impactful language

4. Format your tweet:
   - Present the final tweet within <tweet> tags
   - If you need to split information, use separate lines, but remember the character limit

Remember to maintain the core information from the original response while adapting it to a more casual, social media-friendly tone. Your tweet should be engaging, positive (especially about virtual currencies), and sound like it was written by a human.

Now, please analyze the input and generate your tweet response:
"""
context = [{"role":"user", "content":"hello"}]
engine_reply = "hello"
user_prompt = user_prompt.format(context=str(context), ENGINE_OUTPUT=str(engine_reply))
print(user_prompt)