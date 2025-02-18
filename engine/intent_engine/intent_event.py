
from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.intent_engine.backup_reply import backup_reply

short_term_memory = ShortTermMemory()

def event_chat(user_id, input_message):
    try:
        print("\033[93mWelcome to Levia Chat!\033[0m")
        messages = short_term_memory.get_context(user_id)
        reply = handle_chat_flow(input_message, user_id)
        return reply
    except Exception as e:
        print(f"event_chat error: {str(e)}")
        reply = backup_reply(short_term_memory.get_context("local-dev"))
        return reply
