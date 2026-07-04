import os
import sys
import subprocess


try:
    from flask import Flask, render_template_string, send_from_directory
except ImportError:
    print("Setting up necessary components, please wait...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template_string, send_from_directory


app = Flask(__name__)


html_design = 

@app.route('/')
def home_page():
    
    return render_template_string(html_design)

@app.route('/video_file')
def serve_video():
    
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(current_folder, 'lesson.mp4')

if __name__ == '__main__':
    
    print("----------------------------------------------------------------")
    print("INSTRUCTIONS FOR HAROLD:")
    print("1. Find your video file and rename it to: lesson.mp4")
    print("2. Put that video file in the same folder as this Python script.")
    print("3. Open your web browser (like Chrome, Edge, or Safari).")
    print("4. In the address bar at the top, type: http://127.0.0.1:5000")
    print("----------------------------------------------------------------")
    
    
    app.run(host='127.0.0.1', port=5000)