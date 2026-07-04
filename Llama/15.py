import datetime
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('user_interactions.db')
c = conn.cursor()


c.execute()

def get_user_id():
    
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

@app.route('/track_interaction', methods=['POST'])
def track_interaction():
    data = request.get_json()
    user_id = data['user_id']
    interaction_type = data['interaction_type']

    
    c.execute('INSERT INTO user_interactions (user_id, interaction_type) VALUES (?, ?)',
              (user_id, interaction_type))
    conn.commit()

@app.route('/get_user_interactions', methods=['GET'])
def get_user_interactions():
    user_id = request.args.get('user_id')
    c.execute('SELECT * FROM user_interactions WHERE user_id = ?', (user_id,))
    interactions = c.fetchall()
    return jsonify(interactions)

if __name__ == '__main__':
    app.run(debug=True)