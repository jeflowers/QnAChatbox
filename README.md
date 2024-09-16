# NVIDIA RAG Q&A Chat Application

This application demonstrates a Retrieval-Augmented Generation (RAG) Question & Answer system using NVIDIA AI technologies and LlamaIndex. It allows users to upload documents, process them, and then ask questions based on the content of those documents.

## Features

1. **Embedding Creation**: Utilizes NVIDIA NIM microservices to transform text into high-quality embeddings.
2. **Vector Database**: Employs GPU-accelerated Milvus for efficient storage and retrieval of embeddings.
3. **Inference with Llama3**: Leverages the NIM API's Llama3 model to handle user queries and generate accurate responses.
4. **Orchestration with LlamaIndex**: Integrates and manages all components seamlessly with LlamaIndex for a smooth Q&A experience.

## Prerequisites

- Python 3.7+
- NVIDIA API Key (set as an environment variable `NVIDIA_API_KEY`)

### Getting an NVIDIA API Key

To use this application, you'll need an NVIDIA API key. Follow these steps to obtain one:

1. Visit the NVIDIA AI Foundation Models page: [https://build.nvidia.com/explore/discover](https://build.nvidia.com/explore/discover)
2. If you don't have an NVIDIA account, click on "Sign Up" to create one.
3. Once logged in, navigate to the API section or look for an option to generate an API key.
4. Follow the prompts to create a new API key. You may need to agree to terms of service and select the services you plan to use.
5. Once generated, copy your API key and keep it secure.
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

Remember to replace 'your_api_key_here' with the actual API key you received from NVIDIA.

Note: Keep your API key confidential and do not share it publicly or commit it to version control systems.

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python nchat.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:7860` (or the URL provided in the console output).

3. Use the interface to:
   - Upload documents
   - Load the documents into the system
   - Ask questions based on the loaded documents

## Application Structure

- `nchat.py`: Main application file containing the RAG Q&A system implementation.
- `requirements.txt`: List of Python packages required for the application.

## Key Components

1. **Document Loading**: Uses `SimpleDirectoryReader` to load documents from various file formats.
2. **Vector Store**: Utilizes `MilvusVectorStore` for efficient storage and retrieval of document embeddings.
3. **Embedding Model**: Employs `NVIDIAEmbedding` for creating high-quality text embeddings.
4. **Language Model**: Uses `NVIDIA` LLM (Llama3) for generating responses to user queries.
5. **Index Creation**: Implements `VectorStoreIndex` to create a searchable index of document embeddings.
6. **Query Engine**: Utilizes LlamaIndex's query engine for processing user questions and retrieving relevant information.
7. **User Interface**: Built with Gradio for an easy-to-use web interface.

## Contributing

Contributions to improve the application are welcome. Please follow the standard GitHub pull request process to submit your changes.

## License

MIT License

Copyright (c) 2024 John Flowers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

- NVIDIA for providing the AI technologies used in this application.
- LlamaIndex for the powerful indexing and querying capabilities.
- Gradio for the user interface framework.
