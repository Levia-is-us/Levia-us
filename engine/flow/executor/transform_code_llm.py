from engine.llm_provider.llm import chat_completion
import os

CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")

def transformation_code_llm(input_structure, output_structure, user_id, ch_id):
    prompt = """You are an expert Python developer tasked with creating a function that transforms one data structure into another. Your goal is to create a well-packaged, reusable function that performs the required transformation efficiently and handles potential errors.

Here are the input and output variable structures:

<input_structure>
{INPUT_VARIABLE}
</input_structure>

<output_structure>
{OUTPUT_VARIABLE}
</output_structure>

Please follow these steps to create the transformation function:

1. Analyze the structures:
   In <structure_analysis> tags, provide a detailed analysis of the input and output structures:
   - List and number each key component of both structures
   - Provide a brief example for each component
   - Identify differences between input and output
   - Note required transformations
   - Highlight potential edge cases or challenges

2. Plan the transformation:
   In <transformation_plan> tags, outline your approach:
   - Break down the transformation into sub-tasks
   - Outline steps to transform the input into the output
   - Choose efficient data structures and methods, noting their time and space complexity
   - List potential edge cases and error scenarios
   - Plan for minimal, essential error handling
   - Consider how to make the function robust and reusable

3. Implement the function:
   Based on your analysis and planning, create a Python function that performs the transformation. The function should:
   - Take the input structure as a parameter
   - Implement the transformation logic
   - Return the transformed data in the output structure format
   - Include only essential error handling
   - Be concise, efficient, and ready for production use

Important notes:
- Do not include comments or explanations within the function body
- Aim for the shortest possible character count while maintaining functionality
- The function should be robust and efficient

example:
input_structure:
{{"a":"123","b":"456"}}
output_structure:
["123","456"]
your output should be:
<function>
def transform(input_structure):
   output_structure = [data for data in input_structure.values()]
   return output_structure
</function>

Your final output should be ONLY the Python function, wrapped in <function> tags. Do not include any additional text, explanations, or tests outside of the function definition.
"""
    prompt = prompt.format(INPUT_VARIABLE=input_structure, OUTPUT_VARIABLE=output_structure)
    prompt = [{"role": "user", "content": prompt}]
    response = chat_completion(prompt, model=CHAT_MODEL_NAME, config={"temperature": 0.0}, user_id=user_id, ch_id=ch_id)
    start_tag = '<function>'
    end_tag = '</function>'
    start_index = response.find(start_tag)
    end_index = response.find(end_tag)
    response = response[start_index + len(start_tag):end_index].strip() if start_index != -1 and end_index != -1 else response
    return response

