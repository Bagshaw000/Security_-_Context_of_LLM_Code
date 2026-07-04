import csv
from datetime import datetime
from flask import Flask, request




app = Flask(__name__)


FILE_NAME = 'website_activity.csv'


def setup_spreadsheet():
    try:
        with open(FILE_NAME, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date and Time', 'Web Page Name', 'User Name', 'Action Taken'])
    except FileExistsError:
        
        pass

@app.route('/log_activity')
def log_activity():
    
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    page_name = request.args.get('page', 'Home Page')
    user_name = request.args.get('user', 'Visitor')
    action = request.args.get('action', 'Viewed Page')

    
    with open(FILE_NAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, page_name, user_name, action])

    return "Activity successfully recorded in the spreadsheet"

if __name__ == '__main__':
    setup_spreadsheet()
    print("The tracker is now active and waiting for website visitors.")
    app.run(port=5000)