import csv
from datetime import datetime
from flask import Flask, request




app = Flask(__name__)


def setup_spreadsheet():
    try:
        with open('website_interactions.csv', 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time of Interaction", "User Name", "Page Visited", "Action Taken"])
    except FileExistsError:
        
        pass


@app.route('/log_activity', methods=['POST'])
def log_activity():
    
    
    data = request.json
    
    
    current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    user = data.get('user', 'Guest')
    page = data.get('page', 'Home Page')
    action = data.get('action', 'Viewed Page')

    
    with open('website_interactions.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, user, page, action])
    
    return "The interaction has been recorded in your spreadsheet."


if __name__ == '__main__':
    setup_spreadsheet()
    print("The tracker is now running and waiting for website visitors...")
    app.run()