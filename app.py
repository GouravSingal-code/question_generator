from flask import Flask, request, jsonify
import requests
import subprocess
import time
import os

app = Flask(__name__)

def download_model():
    """Download the model once at startup"""
    try:
        print("Checking if deepseek-r1:1.5b model is available...")
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if 'deepseek-r1:1.5b' not in result.stdout:
            print("Model not found. Downloading deepseek-r1:1.5b...")
            subprocess.run(['ollama', 'pull', 'deepseek-r1:1.5b'], check=True)
            print("Model downloaded successfully!")
        else:
            print("Model deepseek-r1:1.5b already available")
            
    except Exception as e:
        print(f"Error downloading model: {e}")
        raise e

@app.route('/generate', methods=['POST'])
def generate():
    user_text = request.json.get("text", "")
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    
    prompt = f"Generate 3 questions from: {user_text}"

    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "deepseek-r1:1.5b",
            "prompt": prompt
        }, timeout=60)
        
        if res.status_code == 200:
            return jsonify(res.json())
        else:
            return jsonify({"error": f"Ollama API error: {res.status_code}"}), 500
            
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timeout - model may still be loading"}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to Ollama server"}), 500
    except Exception as e:
        return jsonify({"error": f"Generation failed: {str(e)}"}), 500

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
    print("Starting Ollama Question Generator...")
    
    # Wait for Ollama server to start
    print("Waiting for Ollama server to start...")
    time.sleep(10)
    
    # Download model once at startup
    print("Setting up model...")
    download_model()
    
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=7860) 