# Refactored nchat.py

from src.config.config_manager import ConfigManager
from src.data.document_loader import DocumentLoader
from src.storage.vector_store_manager import VectorStoreManager
from src.processing.index_manager import IndexManager
from src.processing.query_processor import QueryProcessor
from src.interface.chat_interface import ChatInterface
from src.interface.gradio_ui_manager import GradioUIManager


class ApplicationManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.document_loader = DocumentLoader()
        self.vector_store_manager = VectorStoreManager()
        self.index_manager = IndexManager()
        self.query_processor = None
        self.chat_interface = None
        self.ui_manager = None

    def initialize(self):
        # Load configuration and set up settings
        self.config_manager.load_config()
        self.config_manager.configure_settings()

        # Initialize UI manager
        self.ui_manager = GradioUIManager(self.document_loader, self.load_documents, self.get_chat_interface)

    def load_documents(self, file_objs):
        try:
            documents, doc_count, file_count = self.document_loader.load_documents(file_objs)

            if not documents:
                return f"No documents found in the selected files."

            vector_store = self.vector_store_manager.create_vector_store()
            storage_context = self.vector_store_manager.create_storage_context(vector_store)

            index = self.index_manager.create_index(documents, storage_context)
            query_engine = self.index_manager.get_query_engine(index)

            self.query_processor = QueryProcessor(query_engine)
            self.chat_interface = ChatInterface(self.query_processor)

            return f"Successfully loaded {doc_count} documents from {file_count} files."
        except Exception as e:
            return f"Error loading documents: {str(e)}"

    def get_chat_interface(self):
        if self.chat_interface is None:
            raise ValueError("Documents must be loaded before chatting.")
        return self.chat_interface

    def run(self):
        self.ui_manager.launch()


'''
def main():
    app_manager = ApplicationManager()
    app_manager.initialize()
    app_manager.run()


if __name__ == "__main__":
    main()
'''