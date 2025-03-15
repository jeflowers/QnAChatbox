# Configuration System Documentation

## Overview

The configuration system in the QnA Chatbox application manages essential settings and external service connections. It primarily handles:

1. API key management for NVIDIA services
2. LlamaIndex settings configuration
3. Model selection and parameters

This document explains the configuration system components, their functionality, and how to customize them for your needs.

## File Structure

The configuration system consists of:

```
src/config/
├── __init__.py                  # Package initialization file
└── config_manager.py            # Main configuration manager class
```

## ConfigManager Class

The `ConfigManager` class is the central component of the configuration system. It provides static methods for configuration management, making them accessible throughout the application without requiring an instance.

### Source Code

```python
import os
from llama_index.core import Settings
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.node_parser import SentenceSplitter


class ConfigManager:
    @staticmethod
    def load_config():
        if os.getenv('NVIDIA_API_KEY') is None:
            raise ValueError("NVIDIA_API_KEY environment variable is not set")

    @staticmethod
    def configure_settings():
        Settings.text_splitter = SentenceSplitter(chunk_size=500)
        Settings.embed_model = NVIDIAEmbedding("NV-Embed-QA", truncate="END")
        Settings.llm = NVIDIA(model="meta/llama-3.1-405b-instruct")

    @staticmethod
    def get_api_key():
        return os.getenv('NVIDIA_API_KEY')
```

## Key Methods

### `load_config()`

```python
@staticmethod
def load_config():
    if os.getenv('NVIDIA_API_KEY') is None:
        raise ValueError("NVIDIA_API_KEY environment variable is not set")
```

This method verifies that the `NVIDIA_API_KEY` environment variable is set. If not, it raises a `ValueError` with a descriptive message. This check is crucial because the application cannot function without access to NVIDIA's AI services.

### `configure_settings()`

```python
@staticmethod
def configure_settings():
    Settings.text_splitter = SentenceSplitter(chunk_size=500)
    Settings.embed_model = NVIDIAEmbedding("NV-Embed-QA", truncate="END")
    Settings.llm = NVIDIA(model="meta/llama-3.1-405b-instruct")
```

This method configures the LlamaIndex global settings with:

1. **Text Splitter**: Sets the `SentenceSplitter` with a chunk size of 500 tokens, determining how documents are divided into smaller pieces for processing
2. **Embedding Model**: Uses NVIDIA's embedding service with the "NV-Embed-QA" model specifically tuned for question-answering tasks
3. **Language Model**: Configures the system to use the "meta/llama-3.1-405b-instruct" model through NVIDIA's API

### `get_api_key()`

```python
@staticmethod
def get_api_key():
    return os.getenv('NVIDIA_API_KEY')
```

A utility method that returns the NVIDIA API key from environment variables. This method provides a centralized way to access the API key throughout the application.

## Usage in the Application

The ConfigManager is primarily used in the ApplicationManager during system initialization:

```python
def initialize(self):
    # Load configuration and set up settings
    self.config_manager.load_config()
    self.config_manager.configure_settings()
```

## Customization Guide

### Changing the Text Splitter Configuration

To modify how documents are split into chunks, edit the `configure_settings()` method:

```python
# For smaller chunks (more granular but more API calls)
Settings.text_splitter = SentenceSplitter(chunk_size=250)

# For larger chunks (fewer API calls but less precise retrieval)
Settings.text_splitter = SentenceSplitter(chunk_size=1000)

# To use different splitting strategies
from llama_index.core.node_parser import TokenTextSplitter
Settings.text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
```

### Using Different NVIDIA Models

To use different NVIDIA models, modify the corresponding lines in `configure_settings()`:

```python
# For a different embedding model
Settings.embed_model = NVIDIAEmbedding("NV-Embed-Large", truncate="END")

# For a different LLM
Settings.llm = NVIDIA(model="mistralai/mixtral-8x7b-instruct-v0.1")
```

### Adding Custom Configuration Parameters

To add new configuration parameters, extend the ConfigManager class:

```python
class ConfigManager:
    # Existing methods...
    
    @staticmethod
    def get_custom_setting():
        return os.getenv('CUSTOM_SETTING', 'default_value')
        
    @staticmethod
    def configure_with_yaml(config_path):
        import yaml
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            # Apply configuration from YAML
            # ...
```

## Environment Variables

The configuration system relies on the following environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| NVIDIA_API_KEY | Yes | API key for accessing NVIDIA AI services |

## Best Practices

1. **Never hardcode API keys** in the config files. Always use environment variables.
2. **Consider using a .env file** for local development, but ensure it's excluded from version control.
3. **Adjust text splitter settings** based on your document characteristics:
   - Use smaller chunks for technical documents where precision is important
   - Use larger chunks for narrative content where context is important
4. **Monitor NVIDIA API usage** to optimize settings for cost and performance.

## Potential Enhancements

1. **Configuration file support**: Add support for YAML or JSON configuration files
2. **Environment-based configuration**: Different settings for development, testing, and production
3. **Dynamic configuration**: Allow some settings to be changed at runtime
4. **Configuration validation**: More comprehensive validation of configuration values
5. **Fallback models**: Support for alternative models if primary ones are unavailable

## Troubleshooting

**Issue**: Error "NVIDIA_API_KEY environment variable is not set"
**Solution**: Ensure the API key is properly set in your environment:
  - For Unix/Linux/macOS: `export NVIDIA_API_KEY=your_key_here`
  - For Windows Command Prompt: `set NVIDIA_API_KEY=your_key_here`
  - For Windows PowerShell: `$env:NVIDIA_API_KEY="your_key_here"`

**Issue**: Model-related errors
**Solution**: Verify that the models specified in `configure_settings()` are available in your NVIDIA account and that you have the necessary permissions.

**Issue**: Text splitting not optimal for your documents
**Solution**: Adjust the chunk size parameter in the `SentenceSplitter` configuration, or consider using a different splitter class from LlamaIndex.
