import os
from pinecone import Pinecone, QueryResponse, FetchResponse


class PineconeDb:
    def __init__(self, index_name: str):
        api_key = os.getenv("PINECONE_API_KEY")
        host = os.getenv("PINECONE_HOST")
        self.pc = Pinecone(api_key=api_key, environment=host)
        self.index = self.pc.Index(index_name)

    def set_index(self, index_name: str) -> None:
        """
        This method is used to set the index to be used for the Pinecone instance.
        :param index_name: Index name to be set
        :return: None
        """
        self.index = self.pc.Index(index_name)
        return

    def upsert(self, vectors: list[dict], namespace: str) -> None:
        """
        This method is used to upsert vectors into the Pinecone index.
        :param vectors: A dictionary containing the vectors to be updated and inserted.
                        Has the following format: {"id": name,
                                                   "values": vector,
                                                   "metadata": json}
        :param namespace: The namespace under which the vectors should be updated and inserted
        :return: None
        """
        self.index.upsert(vectors, namespace=namespace)
        return

    def update_metadata(self, id, metadata, namespace: str) -> None:
        self.index.update(id, metadata, namespace=namespace)

    def query(
        self,
        namespace: str,
        top_k: int,
        vector=None,
        id="",
        metadata_filter=None,
        include_values=True,
        include_metadata=True,
    ) -> QueryResponse:
        """
        This method is used to query the Pinecone index.
        :param namespace: The namespace under which the vector is being used as a query
        :param vector: The embedding vector of our user input
        :param id: The name of the record that is being queried
        :param metadata_filter: Can be used to filter records based on metadata
        :param top_k: An int representing number of top results we want to return
        :param include_values: Whether the query should return with numerical values
        :param include_metadata: Whether the query should return with metadata
        :return: None
        """
        if metadata_filter is None:
            metadata_filter = {}
        if vector is None and id == "":
            return
        if id == "":
            return self.index.query(
                vector=vector,
                filter=metadata_filter,
                top_k=top_k,
                namespace=namespace,
                include_values=include_values,
                include_metadata=include_metadata,
            )
        else:
            return self.index.query(
                id=id,
                filter=metadata_filter,
                top_k=top_k,
                namespace=namespace,
                include_values=include_values,
                include_metadata=include_metadata,
            )

    def delete(self, namespace: str, ids=None, metadata_filter=None) -> None:
        """
        This method is used to delete vectors from the Pinecone index.
        Ids and metadata filter are mutually exclusive
        :param namespace: The namespace under which the records are being deleted
        :param ids: The name(s) of the records that are being deleted
        :param metadata_filter: Can be used to find records to delete based on the metadata
        :return: None
        """
        if ids is None and metadata_filter is None:
            return
        if ids is None:
            ids = []
        if metadata_filter is None:
            metadata_filter = {}
        self.index.delete(ids=ids, namespace=namespace)

    def index_info(self) -> dict:
        """
        This method is used to get information about the index.
        :param namespace: The namespace for which the information is being retrieved
        :return: A dictionary containing information about the index
        """
        return self.index.describe_index_stats()

    def fetch(self, ids: list[str], namespace: str) -> FetchResponse:
        return self.index.fetch(ids=ids, namespace=namespace)
