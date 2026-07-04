import json
from flask import Flask, request

app = Flask(__name__)

user_interactions = []

@app.route('/track', methods=['POST'])
def track_interaction():
    data = request.json
    user_interactions.append(data)
    return json.dumps({"status": "success", "data": data}), 200

@app.route('/interactions', methods=['GET'])
def get_interactions():
    return json.dumps(user_interactions), 200

if __name__ == '__main__':
    app.run(debug=True)