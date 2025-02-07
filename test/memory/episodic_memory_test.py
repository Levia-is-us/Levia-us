import os
import sys
import dotenv

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from memory.episodic_memory.episodic_memory import (
    store_short_pass_memory,
    retrieve_short_pass_memory,
)

# store_short_pass_memory("test", "test", {"test": "test"}, namespace="test")
# store_short_pass_memory("test2", "test2", {"test": "test2"}, namespace="test")

# memories = retrieve_short_pass_memory("test", namespace="test")

memories = retrieve_short_pass_memory("location tool")
print(memories)
