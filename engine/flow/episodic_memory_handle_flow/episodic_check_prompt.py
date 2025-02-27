import datetime
def episodic_check_prompt(user_intent, context, plan):
    date_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    episodic_check_prompt = f"""You are an AI assistant tasked with analyzing user intents, contexts, and plan structures to determine if a given intent can be achieved using the provided plan. Your primary goal is to evaluate the feasibility of the plan and provide appropriate output based on your analysis.

Here is the user's intent:
<user_intent>
{str(user_intent)}
</user_intent>

Now, consider the following context related to the user's intent:
<context>
{str(context)}
</context>

Finally, here is the plan structure you need to analyze:
<plan>
{str(plan)}
</plan>

Note that the realworld time is {date_time}

Please follow these steps to complete your task:

1. Analyze the user intent and context:
   - List key points from the context, quoting relevant parts verbatim
   - Explain how the context relates to the user intent

2. Examine the plan structure and its components:
   - The plan is a list of tool calls, not a traditional plan
   - Each step in the plan should have a structure similar to this:
     {{
       "step": "step number",
       "tool": "ToolName",
       "data": {{
         "method": "method_name",
         "inputs": [
           {{
             "name": "input_name",
             "type": "input_type",
             "required": true/false,
             "description": "input description",
             "source": "source_of_input",
             "method": "method_of_obtaining_input"
           }}
         ],
         "output": {{
           "description": "output description",
           "type": "output_type"
         }}
       }},
       "step purpose": "purpose of this step",
       "description": "description of the step",
       "reason": "reason for this step"
     }}
   - Number and list out each component of the plan structure
   - For each component, explain how it relates to the user intent

3. Attempt to fill in the plan with information from the context:
   - Focus on inputs where "source": "context"
   - cerefuly read the description of the inputs for each step. How them achieving user intent by tool.
   - For each required input, explicitly state whether it is present in the context
   - If the information is available in the context, fill in the "value" field with the appropriate information
   - If the information can not found in the context, leave the "value" field empty
   - Provide a confidence level (high, medium, low) for each piece of information filled in
   - Note any missing information

4. Evaluate the feasibility of the plan to achieve the user's intent:
   - Create a clear list of pros (arguments for the plan's feasibility)
   - Create a clear list of cons (arguments against the plan's feasibility)
   - Weigh the pros and cons to reach a conclusion

Wrap your reasoning for each step inside <input_breakdown> tags. After your analysis, provide your conclusion in one of the following formats:

a) If the plan can be completed with available information and is sufficient to achieve the user intent, output the filled plan as a JSON array. Example:
{{
  "status": "success",
  "plan": [
  {{
    "step": "step 1",
    "tool": "WebSearchTool",
    "data": {{
      "method": "web_search",
      "inputs": [
        {{
          "name": "intent",
          "type": "str",
          "required": true,
          "description": "User's search intention or query context used to generate keywords",
          "source": "context",
          "method": "LLM",
          "value": "the user want to search for the latest news about the stock market"
        }}
      ],
      "output": {{
        "description": "List of relevant URLs or 'No results found' message",
        "type": "Union[List[str], str]"
      }}
    }},
    "step purpose": "Perform a web search to find relevant information",
    "description": "Use the WebSearchTool to execute a web search based on the user's intent",
    "reason": "This step is necessary to gather relevant information that matches the user's intent"
  }}
  ]
}}

b) If any required information is missing, output a JSON object in this format:
{{
  "status": "missing input",
  "name": ["list", "of", "missing", "value", "names"]
}}

c) If you determine that the plan cannot achieve the user intent, output a JSON object in this format:
{{
  "status": "failed",
  "reason": "reason for the failure, why the plan cannot achieve, which steps are not relevant to the user intent"
}}
Important: Only output the JSON object, no other text or comments outside the JSON object.
Now, output the JSON object below:
"""
    propmt = [{"role": "user", "content": episodic_check_prompt}]
    return propmt

