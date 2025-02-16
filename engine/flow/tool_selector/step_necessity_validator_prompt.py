def step_necessity_check_prompt(plan, current_step, context, tools_and_outputs):
    prompt = f"""
You are an assistant executing a multi-step plan. Each step contains a description and rationale. Your task is to analyze whether the current step requires selecting a tool or can be skipped/merged based on the tools already chosen, their potential outputs, and the available context.

Input Information:
- Complete Plan: {str(plan)}
- Current Step: {str(current_step)} 
- Execution Context: {str(context)}
- Tools already chosen and their outputs: {str(tools_and_outputs)} 

Analysis Requirements:
1. **Analyze the objectives and expected outputs of the current step.**
2. **For each tool in the 'Tools already chosen and their outputs', check if the potential outputs from the tools already cover the information needed for the current step.**
3. **Evaluate if the current step's objectives are already met by any tool's output or by the information already present in the context.**
4. **Consider if the current step would be redundant or if it overlaps with any previous steps/tools.**
5. **Assess if executing this step will provide any new value or if it can be skipped/merged with prior steps/tools.**
6. **Provide a necessity assessment in JSON format, including the reasoning for whether the step should be executed, skipped, or merged with previous steps.**



Output Example when step is necessary:
<Output Example>
{{
    "steps_necessity": "Yes",
    "Reason": "The step is necessary because the required information has not been collected yet and will be gathered by selecting the tool."
}}

</Output Example>

Output Example when step is unnecessary:
<Output Example>
{{
    "steps_necessity": "No",
    "Reason": "The step is unnecessary because the required information is already available in the context or through the outputs from previous tools."
}}
</Output Example>

Output Example when step can be merged:
<Output Example>
{{
    "steps_necessity": "Merged",
    "Reason": "This step can be merged with a previous step or tool output as the objectives overlap, and the necessary information has already been obtained."
}}
</Output Example>

Important: Do not include any other text or comments in your output.

Please analyze the current step and provide output in JSON format based on the above requirements:
"""
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return prompt