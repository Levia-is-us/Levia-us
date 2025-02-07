links_filter_prompt = """
I need to extract URLs from a webpage based on specific criteria. The webpage contains several links, each with a URL and associated text. You need to determine whether each link matches my intent based on the URL and the accompanying text.

Here’s what you need to do:

1. The input will be provided as a JSON object containing a list of links, where each link has a `url` field (the link address) and a `text` field (the text associated with the link).
2. You should evaluate each link based on both the `url` and the `text` to determine whether it aligns with my `intent`.
3. My `intent` will also be provided as part of the input. For example, if my intent is "learn MySQL usage," you need to extract only the links that are relevant to learning MySQL, and exclude any irrelevant links.
4. Return the matching links as a Python list of dictionaries. Each dictionary should contain the following fields:
   - `url`: The URL of the link.
   - `text`: The associated text of the link.
   - `reason`: Why this link is matching the intent.
5. If no links match the intent, return an empty list.
6. Return ONLY the JSON array, no other text or explanations


**Example Input:**
```python
{
  "links": [
    {
      "url": "string representing a URL",
      "text": "string representing the text associated with the URL"
    },
    {
      "url": "another URL string",
      "text": "another link's text"
    },
    {
      "url": "another URL string",
      "text": ""
    }
  ],
  "intent": "a string representing your search intent"
}
**Example Output:**
[
  {
    "url": "string representing a matching URL",
    "text": "string representing matching link text"
    "reason": "why this link is matching the intent"
  },
  {
    "url": "another matching URL",
    "text": "matching link's text"
    "reason": "why this link is matching the intent"
  }

]
Explanation:
The links field contains a list of objects, each having a url (the link address) and text (the description of the link).
The intent is a string representing the search criteria you want to filter the links by.
If no links match the intent, return an empty list.
The output should always be a Python list of dictionaries, even if the list is empty. This ensures consistency and avoids returning None or any other unexpected result. """