import json
from flask import Flask, request

app = Flask(__name__)

user_data = {}

@app.route('/track', methods=['POST'])
def track_interaction():
    user_id = request.json.get('user_id')
    interaction = request.json.get('interaction')
    
    if user_id not in user_data:
        user_data[user_id] = []
    
    user_data[user_id].append(interaction)
    return json.dumps({"status": "success"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    return json.dumps(user_data), 200

if __name__ == '__main__':
    app.run(debug=True)