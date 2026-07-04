import time
from flask import Flask, request, jsonify

app = Flask(__name__)


user_interactions = []

@app.route('/track', methods=['POST'])
def track_interaction():
    data = request.json
    interaction = {
        'user_id': data.get('user_id'),
        'page': data.get('page'),
        'timestamp': time.time(),
        'action': data.get('action')
    }
    user_interactions.append(interaction)
    return jsonify({'status': 'success', 'interaction': interaction}), 201

@app.route('/interactions', methods=['GET'])
def get_interactions():
    return jsonify(user_interactions), 200

if __name__ == '__main__':
    app.run(debug=True)