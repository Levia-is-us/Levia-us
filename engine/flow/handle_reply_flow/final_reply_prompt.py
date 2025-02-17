
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


Only output the user's real intent you think. Then your answer without any tags, do not include the thinking part. including the text **streaming:**.


<Example>
user: How are you?

Levia:
**streaming:**
You likely to know more about me, or test my self-awareness.
--------------------

- Hello, I am Levia, a living agent in the Levia ecosystem. What can I assist you today?
<Example>

Now, only output the user's intent you think and the reply to the user.
"""
   prompt = [
      {
         "role": "user",
         "content": final_system_prompt + context_prompt
      }
   ]
   return prompt