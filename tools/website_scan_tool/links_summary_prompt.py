links_summary_prompt = """Please help me summarize the following content, and translate it into a detailed summary based on the overall intention.

Consider the following input:
<input>
{input}
</input>

Requirements:
Identify the intent of the content across all pages (e.g., "News Report," "Product Description," "Technical Documentation," "Blog Post").
Summarize the content from all pages together translate it into a detailed summary based on the overall intention.
The title needs to be accurate
The summary needs to be detailed and fully explained
The summary needs to according to the structure

Return the output in Markdown format:
### Title: News Report
**Summary:** This collection of pages covers recent developments in the tech industry, including the launch of new products, industry challenges, and key shifts in market trends.
Ignore irrelevant content (ads, navigation menus, etc.).
Generate a concise and accurate summary based on the combined content of the pages provided in Markdown format.
"""