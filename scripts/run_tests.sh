#!/bin/bash

# Run unit tests
python -m unittest discover src/tests/unit

# Run integration tests
python -m unittest discover src/tests/integration