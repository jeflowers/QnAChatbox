#!/bin/bash

# Run unit tests
python -m unittest discover tests/unit

# Run integration tests
python -m unittest discover tests/integration
