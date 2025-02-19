import redis
from typing import Any, Optional, List, Dict, Union
import json
from datetime import timedelta
import logging

class ValueOperations:
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
    
    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self._redis.set(key, value, ex=timeout)
        except Exception as e:
            logging.error(f"Error in set: {str(e)}")
            return False
    
    def get(self, key: str) -> Any:
        try:
            value = self._redis.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except (TypeError, json.JSONDecodeError):
                return value
        except Exception as e:
            logging.error(f"Error in get: {str(e)}")
            return None
        
    def increment(self, key: str, delta: int = 1) -> Optional[int]:
        """
        Increment the value of key by delta
        
        Args:
            key: Redis key
            delta: Increment amount (default: 1)
            
        Returns:
            New value after increment or None if failed
        """
        try:
            return self._redis.incrby(key, delta)
        except Exception as e:
            logging.error(f"Error in increment: {str(e)}")
            return None

class HashOperations:
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
    
    def put(self, key: str, hash_key: str, value: Any) -> bool:
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return bool(self._redis.hset(key, hash_key, value))
        except Exception as e:
            logging.error(f"Error in hash put: {str(e)}")
            return False
    
    def get(self, key: str, hash_key: str) -> Any:
        try:
            value = self._redis.hget(key, hash_key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except (TypeError, json.JSONDecodeError):
                return value
        except Exception as e:
            logging.error(f"Error in hash get: {str(e)}")
            return None
    
    def entries(self, key: str) -> Dict[str, Any]:
        try:
            result = self._redis.hgetall(key)
            return {k: self._parse_value(v) for k, v in result.items()}
        except Exception as e:
            logging.error(f"Error in entries: {str(e)}")
            return {}
    
    def _parse_value(self, value: str) -> Any:
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

class ListOperations:
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
    
    def right_push(self, key: str, value: Any) -> Optional[int]:
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self._redis.rpush(key, value)
        except Exception as e:
            logging.error(f"Error in right push: {str(e)}")
            return None
    
    def left_pop(self, key: str) -> Any:
        try:
            value = self._redis.lpop(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except (TypeError, json.JSONDecodeError):
                return value
        except Exception as e:
            logging.error(f"Error in left pop: {str(e)}")
            return None
    
    def range(self, key: str, start: int = 0, end: int = -1) -> List[Any]:
        try:
            values = self._redis.lrange(key, start, end)
            return [self._parse_value(v) for v in values]
        except Exception as e:
            logging.error(f"Error in range: {str(e)}")
            return []
    
    def _parse_value(self, value: str) -> Any:
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

class SetOperations:
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
    
    def add(self, key: str, *values: Any) -> Optional[int]:
        try:
            processed_values = [
                json.dumps(v) if isinstance(v, (dict, list)) else v
                for v in values
            ]
            return self._redis.sadd(key, *processed_values)
        except Exception as e:
            logging.error(f"Error in set add: {str(e)}")
            return None
    
    def members(self, key: str) -> List[Any]:
        try:
            values = self._redis.smembers(key)
            return [self._parse_value(v) for v in values]
        except Exception as e:
            logging.error(f"Error in set members: {str(e)}")
            return []
    
    def _parse_value(self, value: str) -> Any:
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

class RedisTemplate:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True
    ):
        self._redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses
        )
        self._value_ops = ValueOperations(self._redis)
        self._hash_ops = HashOperations(self._redis)
        self._list_ops = ListOperations(self._redis)
        self._set_ops = SetOperations(self._redis)
    
    def opsForValue(self) -> ValueOperations:
        return self._value_ops
    
    def opsForHash(self) -> HashOperations:
        return self._hash_ops
    
    def opsForList(self) -> ListOperations:
        return self._list_ops
    
    def opsForSet(self) -> SetOperations:
        return self._set_ops
    
    def delete(self, key: str) -> bool:
        try:
            return bool(self._redis.delete(key))
        except Exception as e:
            logging.error(f"Error in delete: {str(e)}")
            return False
    
    def hasKey(self, key: str) -> bool:
        try:
            return bool(self._redis.exists(key))
        except Exception as e:
            logging.error(f"Error in hasKey: {str(e)}")
            return False
    
    def expire(self, key: str, timeout: int) -> bool:
        try:
            return bool(self._redis.expire(key, timeout))
        except Exception as e:
            logging.error(f"Error in expire: {str(e)}")
            return False
