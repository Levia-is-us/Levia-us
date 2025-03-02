import datetime

intent_prompt = """Please help me with analyzing user input and generating structured JSON responses. Your goal is to either provide direct answers or summarize user intent for further action.

Here is the conversation input you need to analyze:

<input_messages>
{input_messages}
</input_messages>

Note that the realworld time is:
<time_now>
{time_now}
</time_now>

Please follow these steps to process the input and generate an appropriate response:

1. Analyze the Input:
   - Carefully read and understand the user's request or question.
   - Identify the main topic, context, and any specific information needed to address the input.

2. Determine Response Type:
   - Decide whether you can provide a direct answer based on your knowledge and capabilities.
   - If the request is asking for information, chat, anything that can be answered directly, just help user to do it and provide a direct answer.
   - If the request is asking for actions, tools, anything that can be acted upon by an external system, prepare to summarize the user's intent.
   - If the request is asking for information, but you don't have the information, summarize the user's intent.
   - If the request is unclear or requires actions beyond your abilities (e.g., physical tasks, making purchases), prepare to summarize the user's intent.
   - If the user says something that is unclear and lacks context, you should durect answer and ask further questions.

   
4. Generate Response:
   - For direct answers: Provide a clear, concise response to the user's query.
   - For intent summaries: Summarize the user's goal or request in a way that can be acted upon by an external system.

Before generating your final output, consider the following:
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
    time_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    prompt = [
        {"role": "user", "content": intent_prompt.format(input_messages=input_messages, time_now=time_now)}
    ]
    return prompt