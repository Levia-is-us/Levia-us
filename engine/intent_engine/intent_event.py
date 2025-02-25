
from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.intent_engine.backup_reply import backup_reply
from engine.flow.executor.task_manager import TaskManager
from engine.utils.chat_formatter import create_chat_message
from metacognitive.stream.stream import output_stream
short_term_memory = ShortTermMemory()

task_manager = TaskManager()

def event_chat(user_id, input_message):
    try:
        print("\033[93mWelcome to Levia Chat!\033[0m")
        output_stream(input_message, user_id, "newtask")
        reply = handle_chat_flow(input_message, user_id)
        return reply
    except Exception as e:
        print(f"event_chat error: {str(e)}")
        reply = backup_reply(short_term_memory.get_context(user_id))
        short_term_memory.add_context(
            create_chat_message("assistant", f"{reply}"), user_id
        )
        return reply