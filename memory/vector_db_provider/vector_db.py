from memory.vector_db_provider.pinecone.pinecone import PineconeDb
from datetime import datetime
import time
vector_db = PineconeDb(index_name="levia")


def save_memory(id: str, vector: list, metadata: dict, namespace: str):
    metadata["timestamp"] = int(datetime.now().timestamp() * 1000)
    input_embedding = {
        "id": id,
        "values": vector,
        "metadata": metadata,
    }
    retries = 1
    while retries > 0:
        try:
            vector_db.upsert([input_embedding], namespace)
            break
        except Exception as e:
            print(f"\033[91mError upserting memory: {str(e)}\033[0m")
            retries -= 1
            if retries == 0:
                print(f"\033[91mFailed to upsert memory after 1 retries\033[0m")
            time.sleep(5)


def retrieve_memory(vector: list, namespace: str, top_k: int = 10):
    memories = vector_db.query(
        vector=vector,
        namespace=namespace,
        top_k=top_k,
        include_metadata=True,
        include_values=False,
    )
    return memories

def delete_memory(id: str, namespace: str):
    vector_db.delete(id, namespace)
