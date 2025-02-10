def next_step_prompt(plan, current_step, context):
    prompt_template = f"""You are provided with a workflow consisting of multiple tools. Each tool has a name, method, required arguments, optional arguments, and an expected output. The workflow executes tools sequentially. The input for the workflow may consist of natural language, structured data, key-value pairs, or a mix of these formats. Your task is to evaluate whether the input and the outputs from previously executed tools provide sufficient information to proceed with each tool in the workflow.
Here is the workflow: {str(plan)}
next step is : {str(current_step)}
context is: {str(context)}
For each step in the following workflow:
1. Extract Arguments: Identify all required and optional arguments provided from the input and previous outputs.
2. Validation:
- Confirm if all required arguments for the current tool are satisfied.
- Evaluate if any optional arguments are needed and determine if they can be derived from the context.
Action:
If all required arguments are present and no critical information is missing, only output a json fit the arguments of next format, do not output anything else:
{{
    "step": "<current step number>",
    "can_proceed": true,
    "extracted_arguments": {{
        "required_arguments": {{
            "<argument-name>": "value"
        }}
    }}
}}
If the step cannot proceed, output the following format with details of missing information:
Output your results in the following only JSON format for programmatic processing:
{{
    "step": "<current step number>",
    "can_proceed": false,
    "missing_required_arguments": [<list of missing required arguments>],
    "needed_optional_arguments": [<list of optional arguments that are required>],
    "remarks": "<natural language explanation if applicable>"
}}
"""
    return prompt_template