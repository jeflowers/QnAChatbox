# Google-Style Interface for RAG Q&A Chatbox

This component implements a Google-style search interface for the NVIDIA RAG Q&A Chatbox. It provides a familiar and intuitive way to interact with your documents through both search and chat functionalities.

## Features

- **Google-like Search Interface**: A clean, familiar search UI for querying your documents.
- **Dual-Mode Interaction**: Switch between document search mode and chat mode.
- **Document Upload**: Upload and process documents directly through the interface.
- **Rich Search Results**: View search results with snippets and source information.
- **Conversational Interface**: Engage in a chat conversation about your documents.

## Installation

The Google interface is included as part of the main QnA Chatbox package. No additional installation is required beyond the standard setup for the project.

However, the interface requires Flask, which is included in the updated requirements:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Interface

To start the Google-style interface:

```bash
python google_interface.py
```

This will start the Flask application on port 8080 by default. Open your web browser and navigate to:

```
http://localhost:8080
```

### Command-line Options

The interface supports several command-line options:

```bash
python google_interface.py --host 127.0.0.1 --port 5000 --debug
```

- `--host`: The host to run the server on (default: 0.0.0.0)
- `--port`: The port to run the server on (default: 8080)
- `--debug`: Enable debug mode (disabled by default)

### Using the Interface

#### Document Upload

1. Click on the "Choose File" button to select documents from your computer.
2. Click "Upload & Process" to upload and process the documents.
3. Wait for the confirmation message that the documents have been loaded.

#### Search Mode

1. Enter your query in the search box.
2. Click the "Document Search" button or press Enter.
3. View the search results and the generated answer at the top.
4. Click on individual results to see more context.

#### Chat Mode

1. Click the "Chat Mode" button to switch to the conversational interface.
2. Enter your question in the chat input box.
3. Receive detailed answers generated from your documents.
4. Continue the conversation with follow-up questions.

### Switching Between Interfaces

You can switch between the Google-style interface and the original Gradio interface by running the appropriate script:

- For Google-style interface: `python google_interface.py`
- For original Gradio interface: `python -m src.nchat`

## API Endpoints

The interface provides the following RESTful API endpoints:

- `GET /`: Serves the main page of the Google-style interface.
- `POST /api/upload`: Handles document upload requests.
- `POST /api/search`: Handles search requests.
- `POST /api/chat`: Handles chat message requests.

### API Examples

#### Upload Documents

```javascript
const formData = new FormData();
formData.append('files', fileObject);

fetch('/api/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log(data.message);
});
```

#### Search Documents

```javascript
fetch('/api/search', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: "What is RAG?" })
})
.then(response => response.json())
.then(data => {
    console.log(data.answer);
    console.log(data.results);
});
```

#### Chat

```javascript
fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: "Explain RAG to me" })
})
.then(response => response.json())
.then(data => {
    console.log(data.response);
});
```

## Customization

### Changing the Interface Appearance

The interface appearance is defined in the `templates/google_interface.html` file. You can customize:

- Colors and styling by modifying the CSS
- Logo and branding elements
- Layout and positioning

### Modifying Backend Behavior

The core functionality is implemented in:

- `src/google_interface/google_interface.py`: Core interface class
- `src/google_interface/flask_app.py`: Flask application handling HTTP requests

## Troubleshooting

### Common Issues

1. **Flask Not Starting**:
   - Check if port 8080 is already in use
   - Try a different port with `--port 5000`

2. **Document Upload Errors**:
   - Verify file formats are supported
   - Check file permissions
   - Ensure the temp directory is writable

3. **API Key Issues**:
   - Confirm that the NVIDIA API key is set as an environment variable
   - Check the key has the necessary permissions

### Logs

Check console output for logs. Enable debug mode for more detailed logs:

```bash
python google_interface.py --debug
```

## Integration with Core System

The Google interface integrates with the core QnA Chatbox system through:

- `config_manager.py`: Configuration and API key management
- `document_loader.py`: Document loading and processing
- `vector_store_manager.py`: Vector database management
- `index_manager.py`: Document indexing
- `query_processor.py`: Query processing and response generation

## Architecture

The Google interface follows a modular architecture:

- **Entry Point**: `google_interface.py` initializes components and starts the server
- **Interface Class**: `GoogleStyleInterface` encapsulates core functionality
- **Flask App**: Handles HTTP requests and renders templates
- **HTML/CSS/JS**: Provides the user interface

## Contributing

Contributions to improve the Google interface are welcome. Please see the main project's contribution guidelines.

## License

This project is licensed under the MIT License - see the main project's LICENSE file for details.
