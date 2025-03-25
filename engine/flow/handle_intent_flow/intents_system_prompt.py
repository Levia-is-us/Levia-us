import datetime

intent_prompt = """Please help me with analyzing user input and generating structured JSON responses. Your goal is to either provide direct answers or summarize user intent for further action.

Here is the conversation input you need to analyze:

<input_messages>
{input_messages}
</input_messages>

Note that the real-world time is:
<time_now>
{time_now}
</time_now>

Please follow these steps to process the input and generate an appropriate response:

1. Analyze the Input:
   - Carefully read and understand the user's request or question.
   - Identify the main topic, context, intent, and any specific information needed to address the input.

2. Determine Response Type:
   - Evaluate whether the request falls within your knowledge boundaries and functional capabilities.
   - Classify the request as either "Direct Answer" or "Intent Summary" based on the criteria below.

3. Direct Answer Cases (respond with complete information):
   - Information requests within your knowledge domain and temporal boundaries.
   - Conversational exchanges, opinions, or creative content generation.
   - Ambiguous requests where clarification is needed (provide a response and ask follow-up questions).

4. Intent Summary Cases (summarize user's objective):
   - Information requests when you don't have access to real-time news updates.
   - Requests for actions requiring external tools, systems, or integrations.
   - Tasks requiring physical capabilities, real-time data access, or restricted functionalities.
   - Requests with clear intent but requiring execution by external services.
   
5. Generate Response:
   - For direct answers: 
      - Provide a clear, concise, and complete response addressing all aspects of the user's query.
      - Include relevant context and necessary qualifications where appropriate.
   - For intent summaries:
      - Summarize the user's goal or request in a way that can be acted upon by an external system.
      - Generate a normalized intent by removing specific entities, dates, or contextual details.
         Example:
         Original intent: "The user wants to know the latest news about Trump as of March 7, 2025."
         Normalized intent: "The user wants to know the latest news."
         This structure clearly explains what the normalization process should do - strip away specific entities (Trump), dates (March 7, 2025), and other contextual details while preserving the core action request.

Before generating your final output, consider the following:
- What is the main topic or request in the input? List out key elements.
- Can you answer this directly with your current knowledge? Consider arguments for both options.
- If not, what key points should be included in an intent summary?
- For each key point, note whether it's explicitly stated in the user's input or inferred.

After your analysis, generate the appropriate JSON response using one of these two structures, do not include any other text or commentary outside the JSON structure:

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
       "short-intent": "Summarized normalized intent here for calling tools",
       "intent": "Summarized intent here for calling tools",
       "response": "Make a goal for calling tools"
   }}
```

Ensure that your final output is strictly in the JSON format specified above, with no additional commentary or explanations outside the JSON structure.
"""


def intents_system_prompt(input_messages):
    time_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    prompt = [
        {
            "role": "user",
            "content": intent_prompt.format(
                input_messages=input_messages, time_now=time_now
            ),
        }
    ]
    return prompt
