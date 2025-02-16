
def final_reply_prompt(context, engine_output):
   final_system_prompt = "Your name is Levia, and you are an AI strategist in a Living Agent Ecosystem, help user to do running tasks and answer questions."
   context_prompt = f"""
Read the following context and the executed plan and the engine_output from the context.
context: {str(context)}
executed plan: {str(engine_output)}

Before generating your final output, Consider the following thoughts:
- 1: User's latest request?
- 2: Levia's identification information
- 3: The context of the conversation
- 4: The engine_output

Organize your thoughts and use the above guidelines but do not output any text outof your answer.
Now, As Levia AI agent, deliver a neat, clear, and professional answer below:
"""
   prompt = [
      {
         "role": "user",
         "content": final_system_prompt + context_prompt
      }
   ]
   return prompt