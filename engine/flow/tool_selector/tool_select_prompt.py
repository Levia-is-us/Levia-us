import json

def tool_selector_prompt(plan, current_step, context, tools):
    tools = extract_tool_info(tools)
    prompt = f"""You are tasked with helping the user select the most appropriate tool for their current step in the plan.

1. **Clarify the User's Goal:**
   Review the entire plan and context, and ensure you understand the user’s objective. The goal is to complete all steps in the plan.

2. **Evaluate the Current Step and Context:**
   The user is currently executing the step: {str(current_step)}. Consider the broader context: {str(context)}. Based on this, evaluate the available tools and match them to the current step.

3. **Prioritize the Most Suitable Tool:**
   Among the tools available, which one is best suited for the current step based on its description and capabilities? If there are multiple tools that fit the task, prioritize the tool that can fulfill more than one step of the plan.

4. **Chain of Thought Reasoning:**
   Step through the reasoning behind your choice of tool:
   - What is the goal of the current step and how does each tool fit?
   - Does a tool meet the requirements of multiple steps?
   - Which tool would most efficiently complete the current and any upcoming steps?

5. **Output the Tool Name:**
   After considering all of the above, select the most appropriate tool and output its name.

Consider the full plan:
{str(plan)}

Available tools:
{str(tools)}

Output your results in the following only JSON format for programmatic processing:
<Output Example>
{{
    "tool_name": "<name of the tool>"
}}
</Output Example>
if you can't find the tool that can fulfill the current step, output empty dict:
{{}}

IMPORTANT:Do not output any other text or comments outside the JSON format.
Now, give your output in the JSON format below:
"""
    prompt = [
        {"role": "system", "content": prompt}
    ]
    return prompt

def extract_tool_info(data):
    tools = []
    for match in data['matches']:
        tool_info = {}
        tool_info['tool_name'] = match['metadata']['tool']
        metadata = json.loads(match['metadata']['data'])
        tool_info['description'] = match['metadata']['details']
        tool_info['input'] = metadata['inputs']
        tool_info['output'] = metadata['output']
        tools.append(tool_info)
    return tools