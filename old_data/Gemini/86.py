import csv
from datetime import datetime
from flask import Flask, request, jsonify




app = Flask(__name__)



LOG_FILE = "website_usage_report.csv"

def create_spreadsheet_if_missing():
    
    
    try:
        with open(LOG_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(["Date and Time", "Visitor ID", "Action Taken", "Page Name"])
    except FileExistsError:
        
        pass

@app.route('/log_interaction', methods=['POST'])
def log_interaction():
    
    
    interaction_data = request.get_json()
    
    
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    visitor = interaction_data.get('visitor_name', 'Anonymous')
    action = interaction_data.get('action_type', 'Click')
    location = interaction_data.get('page_url', 'Home Page')

    
    
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, visitor, action, location])

    
    return jsonify({"status": "Information recorded"}), 200

if __name__ == "__main__":
    
    create_spreadsheet_if_missing()
    
    
    
    app.run(port=5000)