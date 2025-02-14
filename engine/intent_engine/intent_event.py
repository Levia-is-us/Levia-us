
from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow
from memory.short_term_memory.short_term_memory import ShortTermMemory

short_term_memory = ShortTermMemory()

def event_chat(input_message:str, user_id: str):
    # TODO: user_id & input_message read from MQ
    user_id = "local-dev"
    input_message = input_message
    print("\033[93mWelcome to Levia Chat!\033[0m")
    messages = short_term_memory.get_context(user_id)
    reply = handle_chat_flow(input_message, user_id)