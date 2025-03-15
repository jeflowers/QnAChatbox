from flask import Flask, request, jsonify, render_template
from src.config.config_manager import ConfigManager
from src.data.document_loader import DocumentLoader


app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')  # If you're using a template file
    # Or if you have the template as a string:
    # return render_template_string(HTML_TEMPLATE)
  
