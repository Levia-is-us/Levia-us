import json
from engine.utils.tokenizer import num_tokens_from_messages
from memory.short_term_memory.short_term_memory_provider.base_context import (
    BaseContextStore,
)


class LocalContextStore(BaseContextStore):
    def __init__(self, max_length=1000):
        """
        Initialize the context store.
        :param max_length: Maximum length of context history to maintain
        """
        self.max_length = max_length
        self.contexts = {}
        # todo: load local json file, TBD
        # with open(
        #     "memory/short_term_memory/short_term_memory_provider/local_context_store/local_context_store.json",
        #     "r",
        # ) as f:
        #     self.contexts = json.load(f)

    def get_context(self, user_key: str = "local"):
        """
        Get current conversation context formatted as string.
        :param user_key: Key to identify user's context
        :return: Current conversation context
        """
        if user_key not in self.contexts:
            return []

        return self.contexts[user_key]

    def add_context(self, context: dict, user_key: str = "local"):
        """
        Add new conversation to history.
        :param context: Context string to add
        :param user_key: Key to identify user's context
        """
        if user_key not in self.contexts:
            self.contexts[user_key] = []

        if isinstance(context, list):
            self.contexts[user_key].extend(context)
        else:
            self.contexts[user_key].append(context)

        # If history exceeds max length, remove oldest entry
        self.auto_delete_context(user_key)
        # todo: write to a local json file
        # with open(
        #     "memory/short_term_memory/short_term_memory_provider/local_context_store/local_context_store.json",
        #     "w",
        # ) as f:
        #     json.dump(self.contexts, f)

    def delete_context(self, context: str, user_key: str = "local"):
        """
        Delete specific context from history.
        :param context: Context string to delete
        :param user_key: Key to identify user's context
        """
        if user_key in self.contexts:
            self.contexts[user_key] = [
                h for h in self.contexts[user_key] if h["user"] != context
            ]

    def auto_delete_context(self, user_key: str = "local"):
        """
        Delete all contexts for a user.
        :param user_key: Key to identify user's context
        """
        context = self.get_context(user_key)
        if not context:
            return

        while num_tokens_from_messages(context) > self.max_length:
            context.pop(
                1
            )  # Pop the second element (index 1) instead of first element (index 0)
