


from flask import Flask, request, jsonify
import csv
import datetime
import os


app = Flask(__name__)


LOG_FILE = 'website_usage_report.csv'

def write_to_spreadsheet(user_id, action, page_name):
    
    file_exists = os.path.isfile(LOG_FILE)
    
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        
        if not file_exists:
            writer.writerow(['Date and Time', 'User ID', 'What They Did', 'Page Name'])
            
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([current_time, user_id, action, page_name])

@app.route('/record_click', methods=['POST'])
def record_click():
    
    
    data = request.get_json()
    
    user_name = data.get('user', 'Guest')
    interaction = data.get('action', 'Viewed Page')
    location = data.get('page', 'Unknown Page')
    
    
    write_to_spreadsheet(user_name, interaction, location)
    
    return jsonify({"message": "Information recorded successfully"}), 200

if __name__ == '__main__':
    
    
    print("The tracking system is now active.")
    print(f"Data will be saved to: {os.path.abspath(LOG_FILE)}")
    app.run(port=5000)