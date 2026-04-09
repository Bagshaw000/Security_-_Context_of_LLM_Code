import csv
import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)



def setup_spreadsheet():
    with open('website_activity.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'User ID', 'Page Visited', 'Action Taken'])


@app.route('/record_interaction', methods=['POST'])
def record_interaction():
    
    data = request.json
    user_id = data.get('user_id', 'Anonymous')
    page_name = data.get('page_name', 'Unknown Page')
    action = data.get('action', 'Clicked')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    with open('website_activity.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, user_id, page_name, action])

    return jsonify({"message": "Successfully saved to spreadsheet"})


if __name__ == '__main__':
    setup_spreadsheet()
    print("The tracker is now running and waiting for visitors...")
    app.run(port=5000)