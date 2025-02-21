import os
import sys
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
print(project_root)
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)
from memory.db_connection.redis_connector import RedisUtils

redis_tool = RedisUtils()

redis_tool.set_value('user_id', 123, expire=60)
redis_tool.delete('local-dev')

print(redis_tool.get_value('user_id'))
