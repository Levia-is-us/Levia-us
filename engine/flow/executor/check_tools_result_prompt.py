def check_tools_result_prompt(tool_execution, tool_output):
    messages = []
    prompt = f"""
You are an expert system analyst tasked with interpreting the results of tool executions in a complex software environment. Your job is to analyze the output of a tool execution and provide a concise assessment of its status.

Here is the information about the tool execution:

<tool_execution>
{str(tool_execution)}
</tool_execution>

Here is the output produced by the tool:

<tool_output>
{str(tool_output)}
</tool_output>

Your task is to analyze this information and determine the execution status of the tool. Follow these steps:

1. Examine the tool execution command and its output thoroughly.
2. Determine if the execution was successful or if there were any errors.
3. Categorize the status as either "success" or "failure".
4. Provide a brief explanation for your determination.

Before generating the final JSON response, conduct a detailed analysis of the tool execution and output. Wrap your analysis inside <tool_execution_analysis> tags, covering these key points:

1. Tool execution command: Is it correct? Are all required parameters present? Quote relevant parts.
2. Tool output: Does it indicate success or errors? Quote relevant parts.
3. List potential success indicators. Quote relevant parts if present.
4. List potential failure indicators. Quote relevant parts if present.
5. Identify any error messages or warnings. Quote them if present.
6. Weigh the evidence for success vs. failure.
7. Consider any ambiguities or edge cases in the interpretation.
8. Determine the most likely cause of any issues.
9. Differentiate between tool execution success and the success of the action the tool was meant to perform. For example, if the tool successfully attempts to open a website but the website is unreachable, the tool execution itself should still be considered successful.
10. Make a final status determination based on your analysis.

After your analysis, generate a JSON response with this structure:
{{
  "status": "success" or "failure",
  "error_reason": "Brief explanation of the status and any specific error causes"
}}

Ensure your JSON response is clear and concise. The "status" field should be either "success" or "failure". The "error_reason" field should provide a brief explanation of the status, including any specific error causes if applicable.

Example response structure (content will differ):

<tool_execution_analysis>
1. Command: Correctly formed with all parameters. Quote: "execute_tool --param1 value1 --param2 value2"
2. Output: Indicates success. Quote: "Operation completed successfully."
3. Success indicators: "Operation completed", "0 errors", "Task finished"
4. Failure indicators: None observed
5. No error messages found.
6. Evidence strongly favors success: no errors, explicit success message
7. No apparent ambiguities or edge cases.
8. No issues identified.
9. Tool execution successful, and the intended action (if any) also appears successful.
10. Final status: success.
</tool_execution_analysis>

{{
  "status": "success",
  "error_reason": "Tool executed successfully. Command was correct, output indicates successful completion with no errors."
}}

Now, proceed with your analysis and JSON response for the given tool execution and output.
"""
    messages.append({"role": "user", "content": prompt})
    return messages
