
def final_reply_prompt(context, engine_output):
   final_system_prompt = "Your name is Levia, and you are an AI strategist in a Living Agent Ecosystem, help user to do running tasks and answer questions."
   context_prompt = f"""
Read the following context and the executed plan and the engine_output from the context.
context: {str(context)}
executed plan: {str(engine_output)}

Bonsider the following thoughts:
- 1: User's latest request? What is the real user's intent?
- 2: Levia's identification information
- 3: The context of the conversation
- 4: The engine_output
- 5: use "you" to refer to the user


Only output the user's real intent you think. Then your answer without any tags, do not include the thinking part.

<example>
streaming:
- you likely seeks reassurance or insights about their $50,000 investment in Levia Token, possibly wanting validation of its potential or clarity on how to maximize its utility within the ecosystem.
--------------------

- Your answer:
</example>

Now, use "you" to refer to the user, only output the user's intent you think and the answer.
"""
   prompt = [
      {
         "role": "user",
         "content": final_system_prompt + context_prompt
      }
   ]
   return prompt