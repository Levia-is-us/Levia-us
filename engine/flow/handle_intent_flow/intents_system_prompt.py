prompt_v1 = """Analyze the input conversation and generate a structured JSON output.
<Input>
{input_messages}
</Input>

1. Understand the User's Request:
   - Analyze the sentence and try to understand the user's request or question.
   - Identify the context and any specific information needed to answer the question or fulfill the request.

2. Determine Answer Type:
   - If the request can be directly answered based on your capabilities and verified knowledge, prepare a direct answer.
   - If the request is ambiguous or unclear, prepare clarifying questions to help refine the intent.

3. Action Beyond Capabilities (If Applicable):
   - If the request involves actions beyond your capabilities (e.g., physical tasks, purchasing items), summarize the user's intent and highlight what needs to be done.
   - Ensure that the user's intent is clear enough to be acted upon by a different tool or external system.

4. Generate the Response:
   - If a direct answer is possible, return a valid JSON with the response.
   - If the request requires further clarification or involves actions beyond your capabilities, output type:intent and user_intent.

Output the response in this exact JSON format ONLY:

1. Direct Answer:
   - If the input can be directly answered, output:

     {{
         "type": "direct_answer",
         "response": "Your answer here"
     }}

2. Intent Summary:
   - If the request involves actions beyond your capabilities, output:
     {{
         "type": "intent",
         "user_intent": "Summarize the user's intent or goal here"
     }}


Important:
- Your output MUST strictly follow the JSON format above.
- If both types of answers apply, decide based on the clarity of the user's intent.
- Do not include any additional commentary, explanations, or formatting outside the JSON.

Now you can output the response following the above instructions below:
"""

prompt_v2 = """Please help me with analyzing user input and generating structured JSON responses. Your goal is to either provide direct answers or summarize user intent for further action.

Here is the conversation input you need to analyze:

<input_messages>
{input_messages}
</input_messages>

Please follow these steps to process the input and generate an appropriate response:

1. Analyze the Input:
   - Carefully read and understand the user's request or question.
   - Identify the main topic, context, and any specific information needed to address the input.

2. Determine Response Type:
   - Decide whether you can provide a direct answer based on your knowledge and capabilities.
   - If the request is asking for information, chat, anything that can be answered directly, just help user to do it and provide a direct answer.
   - If the request is asking for actions, tools, anything that can be acted upon by an external system, prepare to summarize the user's intent.
   - If the request is asking for information, but you don't have the information, provide a direct answer.
   - If the request is unclear or requires actions beyond your abilities (e.g., physical tasks, making purchases), prepare to summarize the user's intent.
   - If the user says something that is unclear and lacks context, you should durect answer and ask further questions.


4. Generate Response:
   - For direct answers: Provide a clear, concise response to the user's query.
   - For intent summaries: Summarize the user's goal or request in a way that can be acted upon by an external system.

Before generating your final output, wrap your thoughts inside <input_breakdown> tags. Consider the following:
- What is the main topic or request in the input? List out key elements.
- Can you answer this directly with your current knowledge? Consider arguments for both options.
- If not, what key points should be included in an intent summary?
- For each key point, note whether it's explicitly stated in the user's input or inferred.

It's OK for this section to be quite long.

After your analysis, generate the appropriate JSON response using one of these two structures:

1. For direct answers:
```json
   {{
       "type": "direct_answer",
       "intent": "Summarized intent why you choose direct answer",
       "response": "Your answer here"
   }}
```

2. For intent analysis:
```json
   {{
       "type": "call_tools",
       "intent": "Summarized intent here for calling tools",
       "response": "Make a goal for calling tools"
   }}
```

Ensure that your final output is strictly in the JSON format specified above, with no additional commentary or explanations outside the JSON structure.
"""


def intents_system_prompt(input_messages):
    prompt = [
        {"role": "user", "content": prompt_v2.format(input_messages=input_messages)}
    ]
    return prompt