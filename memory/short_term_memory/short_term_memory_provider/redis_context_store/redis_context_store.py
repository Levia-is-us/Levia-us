import json
from engine.utils.tokenizer import num_tokens_from_messages
from memory.short_term_memory.short_term_memory_provider.base_context import (
    BaseContextStore,
)
from memory.db_connection.redis_connector import RedisUtils

redis_tool = RedisUtils()

class RedisContextStore(BaseContextStore):
    def __init__(self, max_length=1000):
        """
        Initialize the context store.
        :param max_length: Maximum length of context history to maintain
        """
        self.max_length = max_length

    def get_context(self, user_key: str = "local"):
        """
        Get current conversation context formatted as string.
        :param user_key: Key to identify user's context
        :return: Current conversation context
        """
        context = redis_tool.get_value(user_key)
        if not context:
            return []

        if isinstance(context, str):
            try:
                return json.loads(context)
            except json.JSONDecodeError:
                return []
        else:
            return context   

    def add_context(self, context: dict, user_key: str = "local"):
        """
        Add new conversation to history.
        :param context: Context string to add
        :param user_key: Key to identify user's context
        """
        if context['content'] == '':
            return
        current_context = self.get_context(user_key)
        
        if isinstance(context, list):
            current_context.extend(context)
        else:
            current_context.append(context)

        # If history exceeds max length, remove oldest entry
        self.auto_delete_context(user_key)
        
        redis_tool.set_value(user_key, json.dumps(current_context), expire=60*60*24*3)

    def delete_context(self, context: str, user_key: str = "local"):
        """
        Delete specific context from history.
        :param context: Context string to delete
        :param user_key: Key to identify user's context
        """
        current_context = self.get_context(user_key)
        if current_context:
            current_context = [h for h in current_context if h["user"] != context]
            redis_tool.delete(user_key, json.dumps(current_context))

    def auto_delete_context(self, user_key: str = "local"):
        """
        Delete all contexts for a user.
        :param user_key: Key to identify user's context
        """
        context = self.get_context(user_key)
        if not context:
            return

        while num_tokens_from_messages(context) > self.max_length:
            context.pop(1)  # Pop the second element (index 1) instead of first element (index 0)
            redis_tool.delete(user_key)
