#!/bin/bash

# Build the Docker image
# sudo docker build -t word-to-pdf:latest .

# Run the Docker container
sudo docker run -p 8000:8000 -p 8501:8501 word-to-pdf:latest
