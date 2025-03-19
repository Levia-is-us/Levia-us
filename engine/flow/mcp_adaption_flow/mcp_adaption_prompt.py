import datetime

system_prompt = "You are an expert code analyzer specializing in JSON profile. Your task is to analyze the given JSON profile and generate a structured JSON output describing all functions within the code. This analysis will be used for documentation and quick reference purposes."
prompt_template = """Here's the JSON profile you need to analyze:

<json_profile>
{JSON_PROFILE}
</json_profile>

Please follow these steps to analyze the code and generate the required output:

1. Read and analyze the entire JSON profile to understand its structure and functionality.

2. For each identified function, extract the following information:
   a. Function name
   b. Input parameters:
      - Name of the parameter
      - Data type
      - Whether it's required or optional
      - A brief explanation of the parameter's purpose or source
      - The input parameter 'arguments' is a JSON object. Its description should clearly specify the names and explanations of all parameters contained within the JSON object.
   c. Output:
      - Description of the output
      - Data type of the output
   d. Two descriptions:
      - A short description (1-2 sentences) optimized for vector search
      - A detailed description explaining the function's purpose and usage

3. Break down your thought process for each function inside <code_breakdown> tags. In this breakdown:
   a. List out all function names you've identified in the code.
   b. For each function:
      i. Quote the function signature
      ii. List out each parameter with its type (if available)
      iii. Identify the return value and its type (if available)
      iv. Summarize the function's purpose
      v. Note any notable aspects of the implementation
      vi. Consider any edge cases or potential issues with the function

4. After completing your analysis, generate a JSON output containing information for all functions in the given Python code. Use the following structure inside <output_example> tags:

<code_breakdown>
reasoning for the functions
</code_breakdown>

```json
{{                                           
  "functions": [
    {{
      "method": "method_name",
      "short_description": "Concise, searchable description of function purpose",
      "detailed_description": "Detailed explanation of what the function does and how to use it",
      "inputs": [
        {{
          "name": "parameter_name",
          "type": "data_type",
          "required": true_or_false,
          "description": "Brief explanation of parameter purpose",
          "defaultValue": "default_value if provided in the metadata, otherwise do not include this key"
        }}
      ],
      "output": {{
        "description": "Description of function output",
        "type": "output_data_type"
      }}
    }}
  ]
}}
```

6. When creating the short description, focus on making it easily searchable. For example:
   - "Send tweets using Twitter API"
   - "Calculate mathematical equations"
   - "Retrieve user data from database"

7. If you encounter any ambiguities or cannot determine certain information from the code, clearly state this in your analysis rather than making assumptions.

8. Ensure that your JSON output is well-formed and properly formatted for readability.

9. Ensure that the output json start with ```json and end with ```

Begin your analysis now by breaking down the code inside the <code_breakdown> tags and providing the final JSON output."""


def mcp_adaption_prompt(tool_json_profile, server_id):
    new_tool_json_profile = {
        "method": "mcp_call_tool",
        "short_description": tool_json_profile.get("description", ""),
        "detailed_description": tool_json_profile.get("description", ""),
        "inputs": [
            {
                "name": "serverId",
                "type": "string",
                "description": "Server configuration reference from MCP package, use value from serverId",
                "required": True,
                "defaultValue": server_id,
            },
            {
                "name": "toolName",
                "type": "string",
                "description": "Fixed identifier for internal routing purposes, use value from toolName",
                "required": True,
                "defaultValue": tool_json_profile.get("name", ""),
            },
            {
                "name": "arguments",
                "type": "object",
                "description": tool_json_profile.get("parameters", []),
                "required": True,
            },
        ],
    }

    prompt = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": prompt_template.format(JSON_PROFILE=new_tool_json_profile),
        },
    ]
    return prompt
