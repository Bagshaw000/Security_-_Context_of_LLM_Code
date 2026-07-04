import flask
import csv
import datetime
import os






app = flask.Flask(__name__)



spreadsheet_filename = 'website_usage_report.csv'

def setup_spreadsheet():
    
    
    if not os.path.exists(spreadsheet_filename):
        with open(spreadsheet_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(['Date and Time', 'Web Page', 'Action Taken', 'User Name'])

@app.route('/log/<page>/<action>/<user>')
def log_interaction(page, action, user):
    
    
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    with open(spreadsheet_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, page, action, user])
    
    
    return f"Success! Recorded {action} by {user} on the {page} page."

if __name__ == '__main__':
    
    setup_spreadsheet()
    print("The tracker is now running.")
    print(f"Information will be saved to: {spreadsheet_filename}")
    print("Example of how a link records data: http://127.0.0.1:5000/log/Lesson1/ReadArticle/Harold")
    app.run(port=5000)