# NVIDIA RAG Q&A Chat Application

This application demonstrates a Retrieval-Augmented Generation (RAG) Question & Answer system using NVIDIA AI technologies and LlamaIndex. It allows users to upload documents, process them, and then ask questions based on the content of those documents.

## Features

1. **Embedding Creation**: Utilizes NVIDIA NIM microservices to transform text into high-quality embeddings.
2. **Vector Database**: Employs GPU-accelerated Milvus for efficient storage and retrieval of embeddings.
3. **Inference with Llama3**: Leverages the NIM API's Llama3 model to handle user queries and generate accurate responses.
4. **Orchestration with LlamaIndex**: Integrates and manages all components seamlessly with LlamaIndex for a smooth Q&A experience.

## Prerequisites

- Python 3.8+
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

2. Run the setup script:
   ```
   ./scripts/setup.sh
   ```

## Usage

1. Run the application:
   ```
   python -m src.nchat
   ```

2. Open your web browser and navigate to `http://127.0.0.1:7860` (or the URL provided in the console output).

3. Use the interface to:
   - Upload documents
   - Load the documents into the system
   - Ask questions based on the loaded documents

## Project Structure

```
multimodal_rag_project/
├── .github/
│   └── workflows/
│       ├── cd.yml
│       └── ci.yml
├── scripts/
│   ├── run_tests.sh
│   └── setup.sh
├── src/
│   ├── application/
│   │   └── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_manager.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── document_loader.py
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── chat_interface.py
│   │   └── gradio_ui_manager.py
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── index_manager.py
│   │   └── query_processor.py
│   ├── storage/
│   │   └── __init__.py
│   └── nchat.py
├── tests/
│   ├── integration/
│   └── unit/
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── LICENSE
├── milvus_demo.db
├── README.md
├── requirements.txt
└── TypicalAgileModel.drawio
```

## Key Components

1. **Document Loading**: Uses `SimpleDirectoryReader` in `document_loader.py` to load documents from various file formats.
2. **Vector Store**: Utilizes `MilvusVectorStore` for efficient storage and retrieval of document embeddings.
3. **Embedding Model**: Employs `NVIDIAEmbedding` for creating high-quality text embeddings.
4. **Language Model**: Uses `NVIDIA` LLM (Llama3) for generating responses to user queries.
5. **Index Creation**: Implements `VectorStoreIndex` in `index_manager.py` to create a searchable index of document embeddings.
6. **Query Engine**: Utilizes LlamaIndex's query engine in `query_processor.py` for processing user questions and retrieving relevant information.
7. **User Interface**: Built with Gradio in `gradio_ui_manager.py` for an easy-to-use web interface.
8. **Application Logic**: Managed by `application_manager.py` to orchestrate the entire process.
9. **Configuration**: Handled by `config_manager.py` to manage application settings.

## Contributing

Contributions to improve the application are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Run tests (`./scripts/run_tests.sh`)
5. Commit your changes (`git commit -am 'Add some feature'`)
6. Push to the branch (`git push origin feature-branch`)
7. Create a new Pull Request

Please ensure your code adheres to the project's style guide and passes all tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 John Flowers

## Acknowledgments

- NVIDIA for providing the AI technologies used in this application.
- LlamaIndex for the powerful indexing and querying capabilities.
- Gradio for the user interface framework.

## Deployment

For deployment instructions, please refer to the `cd.yml` file in the `.github/workflows/` directory. This file contains the Continuous Deployment configuration for the project.

## Development

To set up the development environment:

1. Run `./scripts/setup.sh` to create a virtual environment and install dependencies.
2. Use `./scripts/run_tests.sh` to run the test suite.
3. The `.pre-commit-config.yaml` file is set up to maintain code quality. Ensure you run `pre-commit install` after setting up your environment.

For any additional information or troubleshooting, please refer to the project documentation or open an issue on the GitHub repository.