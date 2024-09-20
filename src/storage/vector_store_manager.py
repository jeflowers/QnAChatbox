from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext

class VectorStoreManager:
    @staticmethod
    def create_vector_store():
        return MilvusVectorStore(uri="./milvus_demo.db", dim=1024, overwrite=True)

    @staticmethod
    def create_storage_context(vector_store):
        return StorageContext.from_defaults(vector_store=vector_store)