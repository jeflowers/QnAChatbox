#!/usr/bin/env python
"""
Google Interface Entry Point

This script serves as the entry point for the Google-style interface
of the NVIDIA RAG Q&A Chatbox.
"""

import os
import argparse
import logging
from src.google_interface import GoogleStyleInterface, create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for the Google-style interface.
    Parses command line arguments, initializes the interface,
    and starts the Flask application.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Google-style interface for RAG Q&A Chatbox')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Check for NVIDIA API key
    if 'NVIDIA_API_KEY' not in os.environ:
        logger.warning("NVIDIA_API_KEY environment variable not set. The application may not function correctly.")
    
    try:
        # Initialize the interface
        logger.info("Initializing Google-style interface...")
        interface = GoogleStyleInterface().initialize()
        
        # Create and run the Flask app
        logger.info(f"Starting Flask application on {args.host}:{args.port}...")
        app = create_app(interface)
        app.run(host=args.host, port=args.port, debug=args.debug)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        raise


if __name__ == '__main__':
    main()
