import sqlite3
import uuid
from datetime import datetime
from flask import Flask, request, jsonify





app = Flask(__name__)



def initialize_database():
    
    connection = sqlite3.connect('website_activity.db')
    cursor = connection.cursor()
    
    
    
    
    
    cursor.execute()
    connection.commit()
    connection.close()


initialize_database()




def simple_encrypt(text):
    return text[::-1]



@app.route('/')
def home_page():
    
    
    return 



@app.route('/log_action', methods=['POST'])
def log_action():
    
    data = request.json
    original_action = data.get('action')

    
    
    anonymous_id = "User_" + str(uuid.uuid4())[:4]

    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    encrypted_action = simple_encrypt(original_action)

    
    connection = sqlite3.connect('website_activity.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO activity_log (placeholder_name, action_description, timestamp) VALUES (?, ?, ?)",
        (anonymous_id, encrypted_action, current_time)
    )
    connection.commit()
    connection.close()

    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    
    
    print("The script is active!")
    print("Open your browser and visit: http://127.0.0.1:5000")
    app.run(debug=True)