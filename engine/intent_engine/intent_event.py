
from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.intent_engine.backup_reply import backup_reply
from engine.flow.executor.task_manager import TaskManager
from engine.utils.chat_formatter import create_chat_message
from metacognitive.stream.stream import output_stream
import datetime
import uuid
short_term_memory = ShortTermMemory()

task_manager = TaskManager()

def event_chat(user_id, input_message):
    chid = str(uuid.uuid4())
    try:
        output_stream(input_message, user_id, "newtask", chid)
        reply = handle_chat_flow(input_message, user_id, chid)
        end_time = datetime.datetime.now().timestamp()
        output_stream(log=f"End time: {end_time}", user_id=user_id, type="end_time", ch_id=chid)
        return reply
    except Exception as e:
        print(f"event_chat error: {str(e)}")
        reply = backup_reply(short_term_memory.get_context(user_id), user_id)
        short_term_memory.add_context(
            create_chat_message("assistant", f"{reply}"), user_id
        )
        end_time = datetime.datetime.now().timestamp()
        output_stream(log=f"End time: {end_time}", user_id=user_id, type="end_time", ch_id=chid)
        return reply