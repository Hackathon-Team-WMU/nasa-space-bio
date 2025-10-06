#!/usr/bin/env python3
"""
NASA BioExplorer - Flask API Server

AI Usage Disclosure (NASA Space Apps Challenge 2025):
- This code was developed with assistance from Windsurf AI code assistant
- All AI-generated code was reviewed, tested, and modified by human developers
- See AI_DISCLOSURE.md for complete details
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from llm.llm_rag import query

# create app
app = Flask(__name__)
CORS(app)

# health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# hello world
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

# process query
@app.route('/api/query', methods=['POST'])
def process_query():
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    user_query = data['query']
    role = data['role']

    # Calling langchain rag query
    langchain_response = query(user_query, role)

    return jsonify({
        'query': user_query,
        'role': role,
        'response': langchain_response
    }), 200

# run app
if __name__ == '__main__':
    app.run(debug=True, port=2121)
