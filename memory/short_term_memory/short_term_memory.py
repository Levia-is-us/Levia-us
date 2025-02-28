import threading
from memory.short_term_memory.short_term_memory_provider.local_context_store.local_context_store import (
    LocalContextStore
)
from memory.short_term_memory.short_term_memory_provider.redis_context_store.redis_context_store import (
    RedisContextStore
)

import os
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


class ShortTermMemory:
    _instance = None
    _lock = threading.Lock()  # Ensuring thread safety

    def __new__(cls, max_length: int = 1000):
        with cls._lock:  # Thread-safe instantiation
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(max_length)
        return cls._instance

    def _initialize(self, max_length: int):
        """Initialize the context store."""
        if ENVIRONMENT == "local":
            self.context_store = LocalContextStore(max_length)
        else:
            self.context_store = RedisContextStore(max_length)

    def get_context(self, user_key: str = "local", session_id: str = "local"):
        return self.context_store.get_context(user_key, session_id)

    def add_context(self, context: dict, user_key: str = "local"):
        self.context_store.add_context(context, user_key)

    def delete_context(self, context: str, user_key: str = "local"):
        self.context_store.delete_context(context, user_key)
