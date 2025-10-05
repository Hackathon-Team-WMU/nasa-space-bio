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

    # TODO: call langchain code here like this
    # response = langchain_function(user_query)

    # mock repsonse for starting
    langchain_response = query(user_query)

    return jsonify({
        'query': user_query,
        'response': langchain_response
    }), 200

# run app
if __name__ == '__main__':
    app.run(debug=True, port=2121)
