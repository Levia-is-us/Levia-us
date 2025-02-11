from memory.short_term_memory.short_term_memory_provider.local_context_store.local_context_store import (
    LocalContextStore,
)


class ShortTermMemory:
    def __init__(self, max_length: int = 1000):
        self.context_store = LocalContextStore(max_length)

    def get_context(self, user_key: str = "local"):
        return self.context_store.get_context(user_key)

    def add_context(self, context: dict, user_key: str = "local"):
        self.context_store.add_context(context, user_key)

    def delete_context(self, context: str, user_key: str = "local"):
        self.context_store.delete_context(context, user_key)
