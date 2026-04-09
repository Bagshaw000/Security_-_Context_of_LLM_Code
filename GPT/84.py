import time
from flask import Flask, request, jsonify

app = Flask(__name__)


user_interactions = {}

@app.route('/track', methods=['POST'])
def track_interaction():
    data = request.json
    user_id = data.get('user_id')
    interaction_type = data.get('interaction_type')
    timestamp = time.time()

    if user_id not in user_interactions:
        user_interactions[user_id] = []

    user_interactions[user_id].append({
        'interaction_type': interaction_type,
        'timestamp': timestamp
    })

    return jsonify({'status': 'success'}), 200

@app.route('/interactions/<user_id>', methods=['GET'])
def get_interactions(user_id):
    interactions = user_interactions.get(user_id, [])
    return jsonify(interactions), 200

if __name__ == '__main__':
    app.run(debug=True)