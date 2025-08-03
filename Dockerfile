FROM debian:bookworm-slim

# Install system dependencies
RUN apt update && apt install -y \
    curl git build-essential libssl-dev pkg-config python3 python3-pip \
    && apt clean

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Install Python deps
COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages

# Copy app
COPY app.py .

# Expose default port
EXPOSE 7860

# Start Ollama server and run API
CMD ollama serve & sleep 10 && python3 app.py 