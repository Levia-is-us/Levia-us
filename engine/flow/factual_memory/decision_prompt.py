def decision_prompt(engine_output: list):
    prompt = f"""You are an AI assistant tasked with evaluating information from a tool call flow and its output result to identify valuable knowledge worth recording for future reference. Your goal is to extract reusable information while filtering out irrelevant or unreliable data.

Here is the tool call flow with its output result:
<tool_call_flow>
{str(engine_output)}
</tool_call_flow>

Please analyze the information provided in the tool call flow and output result. Use the following guidelines to determine if there is any knowledge worth recording:

1. Relevance: The information should have a high likelihood of being used again in the future.
2. Reliability: The source must be trustworthy and verifiable.
3. Importance: The knowledge should be significant or of interest to humans.
4. Uniqueness: Prioritize novel information over commonly known facts.
5. Clarity: The information should be clear and easy to understand.

Process:
1. Carefully review the tool call flow and output result.
2. Analyze the information based on the guidelines above.
3. Determine if there is any valuable knowledge worth recording.
4. If valuable knowledge is found, create a Markdown document with an appropriate title.
5. If no valuable knowledge is found, return False.

Before providing your final response, wrap your analysis inside <evaluation> tags. For each guideline, explicitly consider how the information measures up. Then, list any potential knowledge points you've identified, along with a brief explanation of why each point meets or doesn't meet the guidelines. This will help you make a more informed decision about whether there's valuable knowledge to record.

Output Format:
If you find valuable knowledge, provide your response in the following format:
<response>
<title>
[Insert an appropriate title for the knowledge]
</title>
<markdown_document>
[Insert the Markdown formatted document containing the valuable knowledge]
</markdown_document>
</response>

If you do not find any knowledge worth recording, respond with:
<response>
False
</response>

Remember to focus only on knowledge that meets all the guidelines. Do not record unclear, untrustworthy, or trivial information.

Example of desired output structure (generic, for illustration purposes only):
<response>
<title>
[A Concise and Descriptive Title]
</title>
<markdown_document>
# [Main Topic]

## [Subtopic 1]
- [Key point 1]
- [Key point 2]

## [Subtopic 2]
1. [Important fact 1]
2. [Important fact 2]

[Additional relevant information in Markdown format]
</markdown_document>
</response>

Please proceed with your analysis and provide your response accordingly.
"""
    return prompt
