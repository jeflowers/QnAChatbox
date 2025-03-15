"""
Google-style interface for the RAG Q&A Chatbox.
This module provides a class that bridges between the Flask API and the core functionality.
"""

import os
import tempfile
from typing import List, Dict, Any, Tuple

from src.config.config_manager import ConfigManager
from src.data.document_loader import DocumentLoader
from src.storage.vector_store_manager import VectorStoreManager
from src.processing.index_manager import IndexManager
from src.processing.query_processor import QueryProcessor


class GoogleStyleInterface:
    """
    Google-style interface for the RAG Q&A Chatbox.
    
    This class provides methods for document loading, searching, and chat interactions
    in a format suitable for integration with a Google-style search interface.
    """
    
    def __init__(self):
        """Initialize the GoogleStyleInterface with required components."""
        self.config_manager = ConfigManager()
        self.document_loader = DocumentLoader()
        self.vector_store_manager = VectorStoreManager()
        self.index_manager = IndexManager()
        self.query_processor = None
        self.temp_dir = tempfile.mkdtemp()
        self.documents_loaded = False
    
    def initialize(self) -> 'GoogleStyleInterface':
        """
        Initialize components and settings.
        
        Returns:
            GoogleStyleInterface: Self reference for method chaining.
        """
        # Load configuration and set up settings
        self.config_manager.load_config()
        self.config_manager.configure_settings()
        
        return self
    
    def load_documents(self, files) -> Dict[str, Any]:
        """
        Load and process documents from uploaded files.
        
        Args:
            files: List of file objects from Flask's request.files.
            
        Returns:
            Dict[str, Any]: Status information about the document loading process.
        """
        try:
            # Save uploaded files to temp directory
            file_paths = []
            for file in files:
                file_path = os.path.join(self.temp_dir, file.filename)
                file.save(file_path)
                file_paths.append(file_path)
            
            # Load documents
            documents, doc_count, file_count = self.document_loader.load_documents(file_paths)

            if not documents:
                return {"status": "error", "message": "No documents found in the selected files."}

            # Create vector store and storage context
            vector_store = self.vector_store_manager.create_vector_store()
            storage_context = self.vector_store_manager.create_storage_context(vector_store)

            # Create index and query engine
            index = self.index_manager.create_index(documents, storage_context)
            query_engine = self.index_manager.get_query_engine(index)

            # Initialize query processor
            self.query_processor = QueryProcessor(query_engine)
            self.documents_loaded = True

            return {
                "status": "success", 
                "message": f"Successfully loaded {doc_count} documents from {file_count} files."
            }
        except Exception as e:
            return {"status": "error", "message": f"Error loading documents: {str(e)}"}

    def search_documents(self, query: str) -> Dict[str, Any]:
        """
        Search documents using the query processor.
        
        Args:
            query: The search query string.
            
        Returns:
            Dict[str, Any]: Search results and status information.
        """
        if not self.documents_loaded or self.query_processor is None:
            return {"status": "error", "message": "Documents must be loaded before searching."}
        
        try:
            # Use the query processor to search
            response = self.query_processor.process_query(query)
            
            # Format results for search-like display
            # Get source nodes that contributed to answer
            source_nodes = response.source_nodes if hasattr(response, 'source_nodes') else []
            
            results = []
            if source_nodes:
                for i, node in enumerate(source_nodes):
                    title = node.metadata.get('filename', f"Document Section {i+1}") if hasattr(node, 'metadata') else f"Document Section {i+1}"
                    
                    results.append({
                        "title": title,
                        "snippet": node.text[:200] + "..." if len(node.text) > 200 else node.text,
                        "metadata": node.metadata if hasattr(node, 'metadata') else {}
                    })
            
            return {
                "status": "success", 
                "results": results,
                "answer": response.response
            }
        except Exception as e:
            return {"status": "error", "message": f"Error processing query: {str(e)}"}

    def chat(self, message: str) -> Dict[str, Any]:
        """
        Process a chat message using the query processor.
        
        Args:
            message: The chat message string.
            
        Returns:
            Dict[str, Any]: Chat response and status information.
        """
        if not self.documents_loaded or self.query_processor is None:
            return {"status": "error", "message": "Documents must be loaded before chatting."}
        
        try:
            # Use the query processor for chat
            response = self.query_processor.process_query(message)
            return {
                "status": "success",
                "response": response.response if hasattr(response, 'response') else str(response)
            }
        except Exception as e:
            return {"status": "error", "message": f"Error processing message: {str(e)}"}
    
    def cleanup(self) -> None:
        """Clean up temporary files and resources."""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Warning: Failed to clean up temporary directory: {str(e)}")
