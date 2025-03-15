# QnA Chatbox with Google Interface Implementation Guide

This guide provides detailed instructions for implementing a Google-style search interface for the NVIDIA RAG Q&A Chatbox. This implementation transforms the original Gradio interface into a more familiar Google-like search experience while maintaining all the powerful RAG capabilities of the original system.

## Overview

The Google-style interface provides two main modes of interaction:
1. **Search Mode**: Presents document search results in a familiar Google-like format
2. **Chat Mode**: Offers a conversational interface to interact with the documents

## Project Structure Updates

New files and directories have been added to the project:

```
QnAChatbox/
├── google_interface.py                      <-- Entry point for the Google interface
├── docs/
│   └── google_interface_implementation.md   <-- This implementation guide
├── src/
│   ├── google_interface/                    <-- Module for Google interface components
│   │   ├── __init__.py
│   │   ├── flask_app.py                     <-- Flask application
│   │   └── google_interface.py              <-- Core interface class
└── templates/
    └── google_interface.html                <-- HTML template for the interface
```

## Implementation Steps

### 1. Set Up Environment

Ensure you have the required dependencies:

```bash
pip install flask
```

### 2. Complete the Google Interface Module

First, create the `__init__.py` file in the `src/google_interface` directory:

```python
# src/google_interface/__init__.py
from src.google_interface.google_interface import GoogleStyleInterface
from src.google_interface.flask_app import create_app
```

Next, implement the core interface class:

```python
# src/google_interface/google_interface.py
import os
import tempfile

from src.config.config_manager import ConfigManager
from src.data.document_loader import DocumentLoader
from src.storage.vector_store_manager import VectorStoreManager
from src.processing.index_manager import IndexManager
from src.processing.query_processor import QueryProcessor

class GoogleStyleInterface:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.document_loader = DocumentLoader()
        self.vector_store_manager = VectorStoreManager()
        self.index_manager = IndexManager()
        self.query_processor = None
        self.temp_dir = tempfile.mkdtemp()

    def initialize(self):
        # Load configuration and set up settings
        self.config_manager.load_config()
        self.config_manager.configure_settings()
        return self

    def load_documents(self, files):
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

            vector_store = self.vector_store_manager.create_vector_store()
            storage_context = self.vector_store_manager.create_storage_context(vector_store)

            index = self.index_manager.create_index(documents, storage_context)
            query_engine = self.index_manager.get_query_engine(index)

            self.query_processor = QueryProcessor(query_engine)

            return {
                "status": "success", 
                "message": f"Successfully loaded {doc_count} documents from {file_count} files."
            }
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

Next, complete the Flask application:

```python
# src/google_interface/flask_app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
import os

def create_app(interface_instance):
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    
    # Store the interface instance
    app.config['INTERFACE'] = interface_instance
    
    @app.route('/')
    def index():
        return render_template('google_interface.html')
    
    @app.route('/api/upload', methods=['POST'])
    def upload_documents():
        if 'files' not in request.files:
            return jsonify({"status": "error", "message": "No files provided"}), 400
        
        files = request.files.getlist('files')
        result = app.config['INTERFACE'].load_documents(files)
        return jsonify(result)
    
    @app.route('/api/search', methods=['POST'])
    def search():
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"status": "error", "message": "No query provided"}), 400
        
        result = app.config['INTERFACE'].search_documents(data['query'])
        return jsonify(result)
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "No message provided"}), 400
        
        result = app.config['INTERFACE'].chat(data['message'])
        return jsonify(result)
    
    return app
```

### 3. Update the Entry Point Script

Update the root-level Google interface entry point:

```python
# google_interface.py
from src.google_interface import GoogleStyleInterface, create_app

def main():
    # Initialize the interface
    interface = GoogleStyleInterface().initialize()
    
    # Create and run the Flask app
    app = create_app(interface)
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
```

### 4. Update the HTML Template JavaScript

Update the JavaScript in the HTML template to connect to the API:

```javascript
// Replace the mock functions with actual API calls

function handleDocumentUpload() {
    if (!fileInput.files.length) {
        alert('Please select files to upload!');
        return;
    }
    
    uploadStatus.textContent = 'Uploading and processing documents...';
    
    // Create FormData for file upload
    const formData = new FormData();
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('files', fileInput.files[i]);
    }
    
    // Send files to API
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            documentsLoaded = true;
            uploadStatus.textContent = data.message;
        } else {
            uploadStatus.textContent = data.message;
        }
    })
    .catch(error => {
        uploadStatus.textContent = 'Error uploading documents: ' + error;
    });
}

function handleSearch() {
    if (!documentsLoaded) {
        alert('Please upload documents first!');
        return;
    }
    
    const query = searchInput.value.trim();
    if (!query) return;
    
    mainContainer.style.display = 'none';
    resultsContainer.style.display = 'flex';
    headerSearchInput.value = query;
    
    // Show loading indicator
    loadingIndicator.style.display = 'block';
    searchResults.innerHTML = '';
    
    // Send search query to API
    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
        
        if (data.status === 'success') {
            // Display the answer at the top
            if (data.answer) {
                const answerElement = document.createElement('div');
                answerElement.className = 'result-item';
                answerElement.style.backgroundColor = '#f8f9fa';
                answerElement.style.padding = '15px';
                answerElement.style.borderRadius = '8px';
                answerElement.style.marginBottom = '20px';
                
                const answerTitle = document.createElement('div');
                answerTitle.style.fontWeight = 'bold';
                answerTitle.style.marginBottom = '10px';
                answerTitle.textContent = 'Answer:';
                
                const answerText = document.createElement('div');
                answerText.textContent = data.answer;
                
                answerElement.appendChild(answerTitle);
                answerElement.appendChild(answerText);
                searchResults.appendChild(answerElement);
            }
            
            // Display the search results
            displaySearchResults(data.results);
        } else {
            const errorElement = document.createElement('div');
            errorElement.textContent = data.message;
            searchResults.appendChild(errorElement);
        }
    })
    .catch(error => {
        loadingIndicator.style.display = 'none';
        const errorElement = document.createElement('div');
        errorElement.textContent = 'Error searching documents: ' + error;
        searchResults.appendChild(errorElement);
    });
}

function handleHeaderSearch() {
    const query = headerSearchInput.value.trim();
    if (!query) return;
    
    // Show loading indicator
    loadingIndicator.style.display = 'block';
    searchResults.innerHTML = '';
    
    // Send search query to API
    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
        
        if (data.status === 'success') {
            // Display the answer at the top
            if (data.answer) {
                const answerElement = document.createElement('div');
                answerElement.className = 'result-item';
                answerElement.style.backgroundColor = '#f8f9fa';
                answerElement.style.padding = '15px';
                answerElement.style.borderRadius = '8px';
                answerElement.style.marginBottom = '20px';
                
                const answerTitle = document.createElement('div');
                answerTitle.style.fontWeight = 'bold';
                answerTitle.style.marginBottom = '10px';
                answerTitle.textContent = 'Answer:';
                
                const answerText = document.createElement('div');
                answerText.textContent = data.answer;
                
                answerElement.appendChild(answerTitle);
                answerElement.appendChild(answerText);
                searchResults.appendChild(answerElement);
            }
            
            // Display the search results
            displaySearchResults(data.results);
        } else {
            const errorElement = document.createElement('div');
            errorElement.textContent = data.message;
            searchResults.appendChild(errorElement);
        }
    })
    .catch(error => {
        loadingIndicator.style.display = 'none';
        const errorElement = document.createElement('div');
        errorElement.textContent = 'Error searching documents: ' + error;
        searchResults.appendChild(errorElement);
    });
}

function handleChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message
    addUserMessage(message);
    chatInput.value = '';
    
    // Send message to API
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            addBotMessage(data.response);
        } else {
            addBotMessage('Error: ' + data.message);
        }
    })
    .catch(error => {
        addBotMessage('Error: ' + error);
    });
}
```

## Configuration Management

Make sure the NVIDIA API key is properly configured, as it's essential for the application to work. The API key should be set as an environment variable:

```bash
export NVIDIA_API_KEY='your_api_key_here'
```

## Integration with Existing System

The Google interface integrates with the existing system through the following components:

1. **ConfigManager**: Handles the configuration settings, including the NVIDIA API key.
2. **DocumentLoader**: Manages the loading and processing of documents.
3. **VectorStoreManager**: Handles the vector database for efficient storage and retrieval.
4. **IndexManager**: Creates and manages the searchable index.
5. **QueryProcessor**: Processes user queries and generates responses.

## Running the Application

To run the application with the Google interface:

```bash
python google_interface.py
```

This will start the Flask application on port 8080. Open your web browser and navigate to:

```
http://localhost:8080
```

## Testing

1. **Upload Documents**: Start by uploading some documents using the file upload functionality.
2. **Search Mode**: Enter a query in the search box and click the "Document Search" button to see search results.
3. **Chat Mode**: Click the "Chat Mode" button to interact with the documents in a conversational manner.

## Troubleshooting

### Common Issues and Solutions

1. **NVIDIA API Key Error**:
   - Ensure the NVIDIA API key is set as an environment variable.
   - Check that the API key is valid and has the necessary permissions.

2. **File Upload Issues**:
   - Verify that the maximum file size is not exceeded.
   - Ensure the file formats are supported.

3. **Flask Application Not Starting**:
   - Check for port conflicts.
   - Ensure all dependencies are installed.

4. **Empty Search Results**:
   - Verify that documents were successfully loaded.
   - Check the query format and try a different query.

## Conclusion

The Google-style interface provides a familiar and intuitive way to interact with the NVIDIA RAG Q&A system. By following this implementation guide, you can transform the existing system into a more accessible and user-friendly experience, while maintaining all the powerful RAG capabilities of the original system.
