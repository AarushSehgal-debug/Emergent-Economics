from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    response = requests.post(
        'http://localhost:11434/api/generate',
        json=data
    )
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000, debug=False)
    