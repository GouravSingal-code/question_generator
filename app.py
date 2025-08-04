from flask import Flask, request, jsonify
import requests
import subprocess
import time
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_model():
    """Download the model once at startup"""
    try:
        logger.info("Checking if deepseek-r1:1.5b model is available...")
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'deepseek-r1:1.5b' not in result.stdout:
            logger.info("Model not found. Downloading deepseek-r1:1.5b...")
            subprocess.run(['ollama', 'pull', 'deepseek-r1:1.5b'], check=True)
            logger.info("Model downloaded successfully!")
        else:
            logger.info("Model deepseek-r1:1.5b already available")
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        raise e

@app.route('/generate', methods=['POST'])
def generate():
    try:
        user_text = request.json.get("text", "")
        prompt = f"Generate 3 questions from: {user_text}"
        logger.info(f"Received generate request with text: {user_text}")
        try:
            res = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "deepseek-r1:1.5b", "prompt": prompt},
                timeout=60
            )
            res.raise_for_status()
            logger.info("Ollama API call successful.")
            return jsonify(res.json())
        except requests.Timeout:
            logger.error("Ollama API call timed out.")
            return jsonify({"error": "Ollama API call timed out."}), 504
        except requests.RequestException as e:
            logger.error(f"Ollama API call failed: {e}")
            return jsonify({"error": f"Ollama API call failed: {str(e)}"}), 502
    except Exception as e:
        logger.exception("Unexpected error in /generate endpoint.")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/')
def health():
    return "Ollama Question Generator is running."

@app.route('/setup')
def setup():
    """Endpoint to check model status"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'deepseek-r1:1.5b' in result.stdout:
            return "Model is ready!"
        else:
            return "Model not found. Please wait for startup to complete.", 503
    except Exception as e:
        return f"Setup check failed: {str(e)}", 500

if __name__ == '__main__':
    # Wait a bit for Ollama server to start
    time.sleep(10)
    # Ensure model is available
    download_model()
    # Start Flask app
    app.run(host="0.0.0.0", port=7860) 