def get_links_filter_prompt(input: str) -> str:
    links_filter_prompt = f"""
Here's the input containing the links and the intent:

<input>
{input}
</input>

Please follow these instructions carefully:

1. Parse the input JSON object. It contains a list of links and an intent string.

2. For each link in the list, evaluate both the 'url' and 'text' fields to determine if it matches the given intent.

3. Wrap your analysis of each link inside <link_analysis> tags:

<link_analysis>
- Consider the intent: [Restate the intent here]
- List key words/phrases from the intent: [List 3-5 key words or phrases]
- Analyze the URL: 
  * How does the URL structure relate to the intent?
  * Are any key words/phrases present in the URL?
- Analyze the text: 
  * How does the link text relate to the intent?
  * Are any key words/phrases present in the text?
- Compare URL and text to intent:
  * What similarities or relevance do you see?
  * Are there any discrepancies or irrelevant information?
- Determine match: [Decide if this link matches the intent based on the above analysis]
- Confidence rating: [Rate your confidence in the match from 1-10, with 10 being highest]
- If match, provide reason: [Briefly explain why this link matches the intent]
</link_analysis>

4. For each matching link, create a dictionary with the following fields:
   - 'url': The URL of the link
   - 'text': The associated text of the link
   - 'reason': A brief explanation of why this link matches the intent

5. Add each matching link's dictionary to a result list.

6. If no links match the intent, return an empty list.

7. Return the result list as a JSON array. Do not include any additional text or explanations outside of the JSON array.

Example output structure (do not use these specific values):
{
  [{
    "url": "https://example.com/page1",
    "text": "Example link text 1",
    "reason": "This link matches the intent because..."
  },
  {
    "url": "https://example.com/page2",
    "text": "Example link text 2",
    "reason": "This link is relevant to the intent as it..."
  }]
}

Remember, your output must be a valid JSON array containing only the matching links, or an empty array if no links match.
important: Do not include any text outside of the JSON array.
Now, please output your json array below:
"""
    return links_filter_prompt
