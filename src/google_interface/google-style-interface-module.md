# Google-Style Interface Module

This module implements a Google-like search interface for the QnA Chatbox system. It provides a modern, familiar interface for users to search through documents and have conversations about them.

## Overview

The `google_interface` module consists of a Flask application that serves a Google-style web interface and connects it to the core RAG system. This README provides a step-by-step explanation of how the code works.

## File Structure

- `__init__.py` - Module initialization file
- `flask_app.py` - Main Flask application implementing the backend API

## Dependencies

- Flask - Web framework
- Original QnA Chatbox components:
  - ConfigManager
  - DocumentLoader
  - VectorStoreManager
  - IndexManager
  - QueryProcessor

## Code Walkthrough: flask_app.py

### 1. Imports and Setup

```python
import os
from flask import Flask, request, jsonify, render_template
import tempfile

# Import from original project
from src.config.config_manager import ConfigManager
from src.data.document_loader import DocumentLoader
from src.storage.vector_store_manager import VectorStoreManager
from src.processing.index_manager import IndexManager
from src.processing.query_processor import QueryProcessor
```

This section imports the necessary modules:
- Standard Python libraries (os, tempfile)
- Flask components for the web server
- Core components from the original QnA Chatbox system

### 2. Flask Application Initialization

```python
# Create Flask app
app = Flask(__name__, template_folder='../../templates')

# Global variables
query_processor = None
temp_dir = tempfile.mkdtemp()
```

Here we:
- Create a Flask application instance
- Configure it to look for HTML templates in the project's templates directory
- Set up global variables for the query processor and temporary file storage

### 3. GoogleStyleInterface Class

This class serves as a bridge between the Flask API and the core QnA Chatbox functionality.

#### 3.1 Initialization

```python
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
```

This initializes the required components from the core system and loads the configuration.

#### 3.2 Document Loading

```python
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
```

This method:
1. Saves uploaded files to a temporary directory
2. Uses the DocumentLoader to process the files
3. Creates a vector store and storage context
4. Builds a searchable index from the documents
5. Creates a query engine and processor
6. Returns a success or error message

#### 3.3 Search Documents

```python
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
            "answer": response.response if hasattr(response, 'response') else str(response)
        }
    except Exception as e:
        return {"status": "error", "message": f"Error processing query: {str(e)}"}
```

This method:
1. Verifies that documents have been loaded
2. Processes the search query through the query processor
3. Extracts the source nodes that contributed to the answer
4. Formats the results in a search-like display with titles and snippets
5. Returns the formatted results and the answer

#### 3.4 Chat Function

```python
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
```

This method:
1. Verifies that documents have been loaded
2. Processes the chat message through the query processor
3. Returns the response from the RAG system

### 4. Interface Initialization

```python
# Initialize the interface
interface = GoogleStyleInterface()
interface.initialize()
```

This code initializes the GoogleStyleInterface when the module is loaded.

### 5. API Routes

#### 5.1 Main Page Route

```python
@app.route('/')
def index():
    return render_template('google_interface.html')
```

This route serves the main Google-style interface HTML page.

#### 5.2 Document Upload API

```python
@app.route('/api/upload', methods=['POST'])
def upload_documents():
    if 'files' not in request.files:
        return jsonify({"status": "error", "message": "No files provided"}), 400
    
    files = request.files.getlist('files')
    result = interface.load_documents(files)
    return jsonify(result)
```

This API endpoint:
1. Checks if files were provided in the request
2. Gets the list of uploaded files
3. Calls the interface's load_documents method
4. Returns the result as JSON

#### 5.3 Search API

```python
@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"status": "error", "message": "No query provided"}), 400
    
    result = interface.search_documents(data['query'])
    return jsonify(result)
```

This API endpoint:
1. Extracts the search query from the request JSON
2. Verifies that a query was provided
3. Calls the interface's search_documents method
4. Returns the results as JSON

#### 5.4 Chat API

```python
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"status": "error", "message": "No message provided"}), 400
    
    result = interface.chat(data['message'])
    return jsonify(result)
```

This API endpoint:
1. Extracts the chat message from the request JSON
2. Verifies that a message was provided
3. Calls the interface's chat method
4. Returns the response as JSON

### 6. Application Runner

```python
def run_app(host='0.0.0.0', port=8080, debug=True):
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_app()
```

This code:
1. Defines a function to run the Flask application
2. Runs the application if the script is executed directly
3. By default, binds to all interfaces on port 8080 with debug mode enabled

## How To Use

### Direct Execution

You can run the Flask application directly:

```bash
python -m src.google_interface.flask_app
```

### Import and Run from Another Module

```python
from src.google_interface.flask_app import run_app

# Run with default settings
run_app()

# Or customize the host and port
run_app(host='127.0.0.1', port=5000, debug=False)
```

## API Documentation

### Document Upload API

**Endpoint**: `/api/upload`  
**Method**: POST  
**Content Type**: multipart/form-data  
**Parameters**:
- files: List of document files to upload

**Response**:
```json
{
  "status": "success|error",
  "message": "Description of the result"
}
```

### Search API

**Endpoint**: `/api/search`  
**Method**: POST  
**Content Type**: application/json  
**Request Body**:
```json
{
  "query": "Your search query here"
}
```

**Response**:
```json
{
  "status": "success|error",
  "results": [
    {
      "title": "Document Section 1",
      "snippet": "Text snippet from the document...",
      "metadata": {}
    }
  ],
  "answer": "Generated answer to the query"
}
```

### Chat API

**Endpoint**: `/api/chat`  
**Method**: POST  
**Content Type**: application/json  
**Request Body**:
```json
{
  "message": "Your chat message here"
}
```

**Response**:
```json
{
  "status": "success|error",
  "response": "AI-generated response to your message"
}
```

## Error Handling

All API endpoints return appropriate error messages with HTTP status codes:
- 400 Bad Request - When required parameters are missing
- 200 OK - For successful responses, even if there was an internal error (check the "status" field)

## Implementation Notes

1. **Temporary File Storage**: Uploaded files are stored in a temporary directory that is created when the application starts and deleted when it terminates.

2. **State Management**: The query processor is stored both in the interface object and as a global variable for flexibility.

3. **Error Handling**: Comprehensive try/except blocks ensure that errors are caught and reported properly.

4. **Response Format**: All API responses follow a consistent format with status and appropriate data fields.

5. **Adaptation to Original System**: This module adapts the original QnA Chatbox system to work with a web-based interface without modifying the core functionality.

## Next Steps for Development

1. Add user authentication for multi-user support
2. Implement session management to track separate document sets
3. Add document management features (delete, rename, etc.)
4. Enhance result formatting with more metadata from documents
5. Add caching to improve performance for repeated queries
