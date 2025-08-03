from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    user_text = request.json.get("text", "")
    prompt = f"Generate 3 questions from: {user_text}"

    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "deepseek-r1:1.5b",
        "prompt": prompt
    })

    return jsonify(res.json())

@app.route('/')
def health():
    return "Ollama Question Generator is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860) 