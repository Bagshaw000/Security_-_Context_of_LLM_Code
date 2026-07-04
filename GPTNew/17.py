import json
from flask import Flask, request, jsonify

app = Flask(__name__)


user_interactions = []

@app.route('/log_interaction', methods=['POST'])
def log_interaction():
    data = request.get_json()
    
    
    if 'user_id' not in data or 'page' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    interaction = {
        'user_id': data['user_id'],
        'page': data['page'],
        'timestamp': data.get('timestamp', None)
    }
    
    user_interactions.append(interaction)
    return jsonify({'message': 'Interaction logged successfully'}), 201

@app.route('/get_interactions', methods=['GET'])
def get_interactions():
    return jsonify(user_interactions), 200

if __name__ == '__main__':
    app.run(debug=True)