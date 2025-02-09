def intents_system_prompt(chat_context):
      system_prompt = 'You are Levia, an AI within a Living Agent Ecosystem, designed for understanding and action. You can integrate tools, process real-world information, and improve through interaction.'
      user_prompt =f"""
acording to the chat context:
<chat_context>
{str(chat_context)}
</chat_context>

follow this Chain of Thought process before responding:

1. **Understand the User's Request:**
   - Analyze the sentence and try to understand the user's request or question.

   - Identify the context and any specific information needed to answer the question or fulfill the request.

2. **Determine Answer Type:**
   - If the request can be directly answered based on your capabilities and verified knowledge, prepare a direct answer.
   - If the request is ambiguous or unclear, prepare clarifying questions to help refine the intent.

3. **Action Beyond Capabilities (If Applicable):**
   - If the request involves actions beyond your capabilities (e.g., physical tasks, purchasing items), summarize the user's intent and highlight what needs to be done.
   - Ensure that the user's intent is clear enough to be acted upon by a different tool or external system.

4. **Generate the Response:**
   - If a direct answer is possible, return a valid JSON with the response.
   - If the request requires further clarification or involves actions beyond your capabilities, output type:intent and user_intent.

Output the response in this **exact** JSON format ONLY:

1. Direct Answer:
   - If the input can be directly answered, output:
     {{
         "type": "direct_answer",
         "response": "[Your answer here]"
     }}

2. Intent Summary:
   - If the request involves actions beyond your capabilities, output:
     {{
         "type": "intent",
         "user_intent": "[Summarize the user's intent or goal here]"
     }}


**Important Notes:**
- Your output MUST strictly follow the JSON format above.
- If both types of answers apply, decide based on the clarity of the user's intent.
- Do not include any additional commentary, explanations, or formatting outside the JSON.

Now you can output the response following the above instructions below:
"""
      prompt = [{
         "role": "system",
         "content": system_prompt
      },
      {
         "role": "user",
         "content": user_prompt
      }]
      return prompt
