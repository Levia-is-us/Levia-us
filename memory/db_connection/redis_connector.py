import redis
from typing import Any, Optional, Dict, List, Set
from functools import wraps
import json
import time
import ssl

import os
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_DB = os.environ.get("REDIS_DB", "0")
REDIS_MAX_CONNECTIONS = os.environ.get("REDIS_MAX_CONNECTIONS", 20)
REDIS_SSL = os.environ.get("REDIS_SSL", "False")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


class RedisUtils:
    _pool = None
    _default_config = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': REDIS_DB,
        'max_connections': 32,
        'decode_responses': True,
        'socket_timeout': 30,
        'password': REDIS_PASSWORD
    }

    def __init__(self, **kwargs):
        if ENVIRONMENT == "local":
            return
        self.config = {**self._default_config, **kwargs}
        self.connect()

    @classmethod
    def get_pool(cls, config: Optional[Dict] = None) -> redis.ConnectionPool:
        if cls._pool is None:
            effective_config = config if config is not None else cls._default_config
            if REDIS_SSL.lower() == 'true':
                ssl_context = ssl.create_default_context()
                effective_config['connection_class'] = redis.connection.SSLConnection
                effective_config['ssl_cert_reqs'] = ssl.CERT_NONE
            cls._pool = redis.ConnectionPool(**effective_config)
        return cls._pool

    def connect(self) -> redis.Redis:
        try:
            self.client = redis.Redis(connection_pool=self.get_pool())
            self.client.ping()
        except redis.ConnectionError as e:
            raise
        return self.client

    def retry_on_failure(max_retries: int = 3, delay: float = 1):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                retries = 0
                while retries < max_retries:
                    try:
                        return func(self, *args, **kwargs)
                    except (redis.ConnectionError, redis.TimeoutError) as e:
                        retries += 1
                        if retries == max_retries:
                            raise
                        time.sleep(delay)
            return wrapper
        return decorator

    @retry_on_failure()
    def set_value(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        result = self.client.set(key, value, ex=expire)
        return result

    @retry_on_failure()
    def get_value(self, key: str) -> Optional[Any]:
        value = self.client.get(key)
        if value and (value.startswith('{') or value.startswith('[')):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value

    @retry_on_failure()
    def delete(self, key: str) -> int:
        result = self.client.delete(key)
        return result

    @retry_on_failure()
    def list_push(self, key: str, *values: Any) -> int:
        result = self.client.rpush(key, *values)
        return result

    @retry_on_failure()
    def list_pop(self, key: str) -> Optional[str]:
        value = self.client.lpop(key)
        return value

    @retry_on_failure()
    def list_range(self, key: str, start: int = 0, end: int = -1) -> List[str]:
        values = self.client.lrange(key, start, end)
        return values

    @retry_on_failure()
    def hash_set(self, key: str, field: str, value: Any) -> int:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        result = self.client.hset(key, field, value)
        return result

    @retry_on_failure()
    def hash_get(self, key: str, field: str) -> Optional[Any]:
        value = self.client.hget(key, field)
        if value and (value.startswith('{') or value.startswith('[')):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value

    @retry_on_failure()
    def hash_get_all(self, key: str) -> Dict[str, Any]:
        values = self.client.hgetall(key)
        for k, v in values.items():
            if v and (v.startswith('{') or v.startswith('[')):
                try:
                    values[k] = json.loads(v)
                except json.JSONDecodeError:
                    pass
        return values

    @retry_on_failure()
    def set_add(self, key: str, *values: Any) -> int:
        result = self.client.sadd(key, *values)
        return result

    @retry_on_failure()
    def set_members(self, key: str) -> Set[str]:
        members = self.client.smembers(key)
        return members

    def pipeline_execute(self, commands: List[callable]) -> List[Any]:
        pipe = self.client.pipeline()
        for cmd in commands:
            cmd(pipe)
        results = pipe.execute()
        return results

    def close(self):
        if self._pool:
            self._pool.disconnect()

if __name__ == "__main__":
    redis_tool = RedisUtils(host='localhost', port=6379, db=0)

    redis_tool.set_value('user_id', 123, expire=60)
    print(f"User ID: {redis_tool.get_value('user_id')}")

    redis_tool.list_push('tasks', 'task1', 'task2')
    print(f"Tasks: {redis_tool.list_range('tasks')}")

    redis_tool.hash_set('user:1', 'name', 'Alice')
    redis_tool.hash_set('user:1', 'data', {'age': 25})
    print(f"User name: {redis_tool.hash_get('user:1', 'name')}")
    print(f"User all: {redis_tool.hash_get_all('user:1')}")

    redis_tool.set_add('tags', 'python', 'redis')
    print(f"Tags: {redis_tool.set_members('tags')}")

    results = redis_tool.pipeline_execute([
        lambda p: p.set('pipe_key', 'pipe_value'),
        lambda p: p.get('pipe_key')
    ])
    print(f"Pipeline results: {results}")

    redis_tool.close()