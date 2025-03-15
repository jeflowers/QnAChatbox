"""
Google-style interface module for the RAG Q&A Chatbox.

This module provides components for implementing a Google-style search interface
for the NVIDIA RAG Q&A Chatbox.
"""

from src.google_interface.google_interface import GoogleStyleInterface
from src.google_interface.flask_app import create_app

__all__ = ['GoogleStyleInterface', 'create_app']
