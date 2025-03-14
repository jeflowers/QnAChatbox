# Google-Style Interface for NVIDIA RAG Q&A Chatbox

This project enhances the original [QnAChatbox](https://github.com/jeflowers/QnAChatbox.git) by implementing a Google-like search interface on top of the powerful RAG (Retrieval-Augmented Generation) system.

## Features

- **Google-like Search Interface**: Clean, familiar search interface inspired by Google's design
- **Dual Mode Operation**: 
  - Search mode for quickly finding relevant document sections
  - Chat mode for detailed Q&A with the AI about your documents
- **Document Upload**: Easy document uploading and processing
- **AI-Powered Results**: Leverages NVIDIA AI and LlamaIndex for intelligent document processing and responses

## Prerequisites

- Python 3.8+
- NVIDIA API Key (set as an environment variable `NVIDIA_API_KEY`)
- Original QnAChatbox repository cloned and set up

### Getting an NVIDIA API Key

To use this application, you'll need an NVIDIA API key. Follow these steps to obtain one:

1. Visit the NVIDIA AI Foundation Models page: [https://build.nvidia.com/explore/discover](https://build.nvidia.com/explore/discover)
2. If you don't have an NVIDIA account, click on "Sign Up" to create one
3. Once logged in, navigate to the API section or look for an option to generate an API key
4. Follow the prompts to create a new API key (you may need to agree to terms of service and select the services you plan to use)
5. Copy your API key and keep it secure
6. Set the API key as an environment variable on your system:
   - On Unix-based systems (Linux, macOS):
     ```
     export NVIDIA_API_KEY='your_api_key_here'
     ```
   - On Windows (Command Prompt):
     ```
     set NVIDIA_API_KEY=your_api_key_here
     ```
   - On Windows (PowerShell):
     ```
     $env:NVIDIA_API_KEY='your_api_key_here'
     ```

**Important Notes**:
- Keep your API key confidential and do not share it publicly or commit it to version control systems
- Be aware of any usage limits or costs associated with your NVIDIA account
- The API key may have an expiration date, so check NVIDIA's documentation for details on key management

## Installation

1. Clone the original repository:
   ```
   git clone https://github.com/jeflowers/QnAChatbox.git
   cd QnAChatbox
   ```

2. Run the setup script from the original repository:
   ```
   ./scripts/setup.sh
   ```

3. Copy the new Google interface files into the repository:
   - Copy `google_interface.py` to the project root directory
   - Create a `templates` directory and add the HTML template to it

## Usage

1. Run the Google-style interface:
   ```
   python google_interface.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:8080`

3. Upload documents using the interface:
   - Click "Choose Files" and select your documents
   - Click "Upload & Process" to load them into the system

4. Use the search interface:
   - Enter your query in the search box
   - Click "Document Search" or press Enter
   - Browse the search results

5. Or use chat mode:
   - Click "Chat Mode" button
   - Type your questions in the chat input
   - Receive detailed answers from the AI based on your documents

## How It Works

1. **Document Processing**: 
   - When you upload documents, they're processed using LlamaIndex and NVIDIA AI
   - Documents are transformed into vector embeddings for efficient search

2. **Search Mode**:
   - Your query is used to find the most relevant sections of your documents
   - Results are displayed in a Google-like format with snippets

3. **Chat Mode**:
   - Maintains conversation context for more interactive Q&A
   - Uses RAG to provide accurate answers based on your documents

## Customization

You can customize the interface by modifying the HTML template:

- Edit colors, fonts, and layout in the CSS section
- Change the logo and branding elements
- Adjust the search and chat UI components

## Integration with Existing System

This interface integrates with the original QnAChatbox system by:

1. Using the same document loading and processing pipeline
2. Leveraging the same vector store and index management
3. Using the same query processing system
4. Adding a new web interface layer using Flask instead of Gradio

## Troubleshooting

If you encounter issues:

1. Ensure NVIDIA API Key is properly set
2. Check that all dependencies are installed
3. Verify that documents are in supported formats
4. Check the console/terminal for error messages

## License

This project maintains the MIT License from the original repository.

## Acknowledgments

- Original QnAChatbox by John Flowers
- NVIDIA for AI technologies
- LlamaIndex for document indexing and retrieval capabilities
