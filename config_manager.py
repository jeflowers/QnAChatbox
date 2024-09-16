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