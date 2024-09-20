#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks
pip install pre-commit
pre-commit install

# Create necessary directories
mkdir -p src/{application,config,data,interface,processing,storage}
touch src/{application,config,data,interface,processing,storage}/__init__.py

echo "Environment setup complete. Activate it with 'source venv/bin/activate'"