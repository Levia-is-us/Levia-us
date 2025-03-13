import redis
from typing import Any, Optional, Dict, List, Set, Union
from functools import wraps
import json
import time
import ssl

import os
import redis.client
import redis_lock
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_DB = os.environ.get("REDIS_DB", "0")
REDIS_MAX_CONNECTIONS = os.environ.get("REDIS_MAX_CONNECTIONS", 20)
REDIS_SSL = os.environ.get("REDIS_SSL", "False")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


class RedisUtils:
    _instance = None
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

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, **kwargs):
        if self._initialized:
            return
            
        if ENVIRONMENT == "local":
            self._initialized = True
            return
            
        self.config = {**self._default_config, **kwargs}
        self.connect()
        self._initialized = True

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
    def get_json_value(self, key: str) -> Optional[Any]:
        if ENVIRONMENT != "local":
            value = self.client.get(key)
            if value and (value.startswith('{') or value.startswith('[')):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    pass
        return ""
    
    @retry_on_failure()
    def get_value(self, key: str) -> Optional[Any]:
        if ENVIRONMENT != "local":
            value = self.client.get(key)
            return value
        return ""

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

    def get_lock(self, name: str, expire: int = 1800) -> redis_lock.Lock:
         return redis_lock.Lock(redis_client=self.client, name=name, expire=expire)

    @retry_on_failure()
    def publish(self, channel: str, message: Any) -> int:
        """
        Publish a message to the specified channel
        """
        if isinstance(message, (dict, list)):
            message = json.dumps(message)
        return self.client.publish(channel, message)
    
    def pubsub(self) -> redis.client.PubSub:
        if ENVIRONMENT == "local":
            return None
        return self.client.pubsub(ignore_subscribe_messages=True)

    def subscribe(self, channels: Union[str, List[str]]) -> redis.client.PubSub:
        """
        Subscribe to one or more channels
        Returns a PubSub object that can be used to listen for messages
        """
        pubsub = self.client.pubsub()
        pubsub.subscribe(channels)
        return pubsub

    def pattern_subscribe(self, patterns: Union[str, List[str]]) -> redis.client.PubSub:
        """
        Subscribe to channels using pattern matching
        Example: 'channel.*' will match all channels starting with 'channel.'
        """
        pubsub = self.client.pubsub()
        pubsub.psubscribe(patterns)
        return pubsub

    def unsubscribe(self, pubsub: redis.client.PubSub, channels: Union[str, List[str]] = None) -> None:
        """
        Unsubscribe from specified channels
        If channels is None, unsubscribe from all channels
        """
        if channels is None:
            pubsub.unsubscribe()
        else:
            pubsub.unsubscribe(channels)

    def pattern_unsubscribe(self, pubsub: redis.client.PubSub, patterns: Union[str, List[str]] = None) -> None:
        """
        Unsubscribe from pattern subscriptions
        If patterns is None, unsubscribe from all patterns
        """
        if patterns is None:
            pubsub.punsubscribe()
        else:
            pubsub.punsubscribe(patterns)

    @retry_on_failure()
    def setex(self, key: str, time: int, value: Any) -> bool:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.setex(key, time, value)

    @retry_on_failure()
    def exists(self, key: str) -> bool:
        return bool(self.client.exists(key))

    @retry_on_failure()
    def expire(self, key: str, time: int) -> bool:
        return bool(self.client.expire(key, time))

    @retry_on_failure()
    def ismember(self, key: str, value: Any) -> bool:
        """
        Check if value is a member of the set stored at key
        
        Args:
            key: The Redis key of the set
            value: The value to check for membership
            
        Returns:
            bool: True if the value is a member of the set, False otherwise
        """
        return bool(self.client.sismember(key, value))
