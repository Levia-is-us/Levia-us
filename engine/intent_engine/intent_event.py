from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow
from memory.short_term_memory.short_term_memory import ShortTermMemory
from engine.intent_engine.backup_reply import backup_reply
from engine.flow.executor.task_manager import TaskManager
from engine.utils.chat_formatter import create_chat_message
from metacognitive.stream.stream import output_stream
import datetime
import uuid
import redis_lock
from memory.db_connection.redis_connector import RedisUtils
short_term_memory = ShortTermMemory()
task_manager = TaskManager()
redis_tool = RedisUtils()

def event_chat(user_id, input_message, session_id: str = ""):
    chid = str(uuid.uuid4())
    lock = redis_tool.get_lock("levia_chat_lock_" + user_id + session_id, 1800)
    try:
        if lock.acquire(blocking=False):
            try:
                output_stream(input_message, user_id, "newtask", chid)
                reply = handle_chat_flow(input_message, user_id, chid, session_id)
                end_time = datetime.datetime.now().timestamp()
                output_stream(log=f"End time: {end_time}", user_id=user_id, type="end_time", ch_id=chid)
                return reply
            finally:
                lock.release()
        else:
            output_stream(log="The current user session is still active. Please try again later.", user_id=user_id, type="think", ch_id=chid)
            return "The current user session is still active. Please try again later."
    except Exception as e:
        print(f"event_chat error: {str(e)}")
        reply = backup_reply(short_term_memory.get_context(user_id), user_id, chid)
        short_term_memory.add_context(
            create_chat_message("assistant", f"{reply}"), user_id
        )
        end_time = datetime.datetime.now().timestamp()
        output_stream(log=f"End time: {end_time}", user_id=user_id, type="end_time", ch_id=chid)
        return reply