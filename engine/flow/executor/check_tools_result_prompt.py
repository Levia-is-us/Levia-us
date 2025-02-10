def check_tools_result_prompt(tool_execution, tool_output):
    messages = []
    prompt = f"""Analyze the tool's output and generate a JSON response with the following structure:

                                    - status: The execution status of the tool, categorized as one of the following:
                                    1. success: Tool executed successfully, including errors caused by incorrect parameters.
                                    2. tool_error: Tool execution failed due to a code-related error.
                                    3. unknown_error: Unable to determine the status from the output.
                                    - error_reason: A detailed explanation of the status and, if applicable, the specific cause of the error.
                                    Ensure the JSON response is clear, structured, and easy to parse.
                                    """
    messages.append({"role": "assistant", "content": prompt})
    messages.append({"role": "user", "content": f"tool_execution: {tool_execution}, tool_output: {tool_output}"})
    return messages
