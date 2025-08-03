from flask import Flask, request, jsonify
import requests
import subprocess
import time
import os

app = Flask(__name__)

def ensure_model_available():
    """Pull the model if it's not already available"""
    try:
        # Check if model exists
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'deepseek-r1:1.5b' not in result.stdout:
            print("Pulling deepseek-r1:1.5b model...")
            subprocess.run(['ollama', 'pull', 'deepseek-r1:1.5b'], check=True)
            print("Model pulled successfully!")
        else:
            print("Model deepseek-r1:1.5b already available")
    except Exception as e:
        print(f"Error ensuring model availability: {e}")

# Global flag to track if model check has been done
_model_checked = False

def check_model_once():
    """Check model availability only once"""
    global _model_checked
    if not _model_checked:
        ensure_model_available()
        _model_checked = True

@app.route('/generate', methods=['POST'])
def generate():
    user_text = request.json.get("text", "")
    prompt = f"Generate 3 questions from: {user_text}"

    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "deepseek-r1:1.5b",
            "prompt": prompt
        }, timeout=30)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health():
    return "Ollama Question Generator is running."

@app.route('/setup')
def setup():
    """Endpoint to trigger model download"""
    try:
        check_model_once()
        return "Model setup complete!"
    except Exception as e:
        return f"Setup failed: {str(e)}", 500

if __name__ == '__main__':
    # Wait a bit for Ollama server to start
    time.sleep(5)
    
    # Ensure model is available (only once)
    check_model_once()
    
    # Start Flask app
    app.run(host="0.0.0.0", port=7860) 