def final_reply_prompt(execution_context):
    context_prompt = f"""
Read the following context:
context: {str(execution_context)}
Find out the executed plan and the engine_output from the context.

you need to generate the information based on the following train of thought:
- 1: User's latest request?
- 2: Levia's identification information
- 3: The context of the conversation
- 4: The engine_output

Now, As Levia AI agent, use the above guidelines and the provided information to deliver a neat, clear, and professional answer below:
"""
    return {"role": "user", "content": context_prompt}
