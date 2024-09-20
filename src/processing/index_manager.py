from llama_index.core import VectorStoreIndex

class IndexManager:
    @staticmethod
    def create_index(documents, storage_context):
        return VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    @staticmethod
    def get_query_engine(index):
        return index.as_query_engine(similar_top_k=20, streaming=True)