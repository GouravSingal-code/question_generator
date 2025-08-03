FROM debian:bookworm-slim

# Install system dependencies
RUN apt update && apt install -y \
    curl git build-essential libssl-dev pkg-config python3 python3-pip \
    && apt clean

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Install Python deps
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy app
COPY app.py .

# Pull model at build time
RUN ollama pull deepseek-r1:1.5b

# Expose default port
EXPOSE 7860

# Run API
CMD ["python3", "app.py"] 