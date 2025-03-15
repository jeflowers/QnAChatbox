# google_interface.py
import os
from flask import Flask, request, jsonify, send_from_directory, render_template_string
import tempfile

# Import from original project
from src.config.config_manager import ConfigManager
from src.data.document_loader import DocumentLoader
from src.storage.vector_store_manager import VectorStoreManager
from src.processing.index_manager import IndexManager
from src.processing.query_processor import QueryProcessor

# Create Flask app
app = Flask(__name__)

# Global variables
query_processor = None
temp_dir = tempfile.mkdtemp()
HTML_TEMPLATE = """<!DOCTYPE html>..."""  # Paste the HTML content here

class GoogleStyleInterface:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.document_loader = DocumentLoader()
        self.vector_store_manager = VectorStoreManager()
        self.index_manager = IndexManager()
        self.query_processor = None

    def initialize(self):
        # Load configuration and set up settings
        self.config_manager.load_config()
        self.config_manager.configure_settings()

    def load_documents(self, files):
        try:
            # Save uploaded files to temp directory
            file_paths = []
            for file in files:
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                file_paths.append(file_path)

            # Load documents
            documents, doc_count, file_count = self.document_loader.load_documents(file_paths)

            if not documents:
                return {"status": "error", "message": "No documents found in the selected files."}

            vector_store = self.vector_store_manager.create_vector_store()
            storage_context = self.vector_store_manager.create_storage_context(vector_store)

            index = self.index_manager.create_index(documents, storage_context)
            query_engine = self.index_manager.get_query_engine(index)

            self.query_processor = QueryProcessor(query_engine)
            
            # Set global query processor
            global query_processor
            query_processor = self.query_processor

            return {"status": "success", "message": f"Successfully loaded {doc_count} documents from {file_count} files."}
        except Exception as e:
            return {"status": "error", "message": f"Error loading documents: {str(e)}"}

    def search_documents(self, query):
        if self.query_processor is None:
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
                    results.append({
                        "title": f"Document Section {i+1}",
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

    def chat(self, message):
        if self.query_processor is None:
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

# Initialize the interface
interface = GoogleStyleInterface()
interface.initialize()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/upload', methods=['POST'])
def upload_documents():
    if 'files' not in request.files:
        return jsonify({"status": "error", "message": "No files provided"}), 400
    
    files = request.files.getlist('files')
    result = interface.load_documents(files)
    return jsonify(result)

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"status": "error", "message": "No query provided"}), 400
    
    result = interface.search_documents(data['query'])
    return jsonify(result)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"status": "error", "message": "No message provided"}), 400
    
    result = interface.chat(data['message'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
