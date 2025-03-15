"""
Flask application for the Google-style interface.
This module provides a Flask application that serves the Google-style interface
and handles API requests for document loading, searching, and chat.
"""

import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from typing import Dict, Any

from src.google_interface.google_interface import GoogleStyleInterface


def create_app(interface_instance: GoogleStyleInterface) -> Flask:
    """
    Create and configure a Flask application for the Google-style interface.
    
    Args:
        interface_instance: An initialized GoogleStyleInterface instance.
        
    Returns:
        Flask: The configured Flask application.
    """
    # Create Flask app with the templates folder in the project root
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    
    # Store the interface instance
    app.config['INTERFACE'] = interface_instance
    
    @app.route('/')
    def index() -> str:
        """
        Serve the main page of the Google-style interface.
        
        Returns:
            str: Rendered HTML template.
        """
        return render_template('google_interface.html')
    
    @app.route('/api/upload', methods=['POST'])
    def upload_documents() -> Dict[str, Any]:
        """
        Handle document upload requests.
        
        Returns:
            Dict[str, Any]: JSON response with status information.
        """
        if 'files' not in request.files:
            return jsonify({"status": "error", "message": "No files provided"}), 400
        
        files = request.files.getlist('files')
        result = app.config['INTERFACE'].load_documents(files)
        return jsonify(result)
    
    @app.route('/api/search', methods=['POST'])
    def search() -> Dict[str, Any]:
        """
        Handle search requests.
        
        Returns:
            Dict[str, Any]: JSON response with search results.
        """
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"status": "error", "message": "No query provided"}), 400
        
        result = app.config['INTERFACE'].search_documents(data['query'])
        return jsonify(result)
    
    @app.route('/api/chat', methods=['POST'])
    def chat() -> Dict[str, Any]:
        """
        Handle chat message requests.
        
        Returns:
            Dict[str, Any]: JSON response with chat response.
        """
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "No message provided"}), 400
        
        result = app.config['INTERFACE'].chat(data['message'])
        return jsonify(result)
    
    @app.errorhandler(404)
    def not_found(e) -> tuple:
        """
        Handle 404 errors.
        
        Args:
            e: The exception object.
            
        Returns:
            tuple: JSON response with error message and status code.
        """
        return jsonify({"status": "error", "message": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e) -> tuple:
        """
        Handle 500 errors.
        
        Args:
            e: The exception object.
            
        Returns:
            tuple: JSON response with error message and status code.
        """
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    
    return app
