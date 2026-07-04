import os
from flask import Flask, render_template_string, send_from_directory








app = Flask(__name__)


VIDEO_FOLDER = 'videos'
if not os.path.exists(VIDEO_FOLDER):
    os.makedirs(VIDEO_FOLDER)


HTML_LAYOUT = 

@app.route('/')
def home_page():
    
    files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith('.mp4')]
    return render_template_string(HTML_LAYOUT, video_files=files)

@app.route('/watch/<filename>')
def watch_page(filename):
    
    return render_template_string(HTML_LAYOUT, playing_now=filename)

@app.route('/stream/<filename>')
def stream_file(filename):
    
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == '__main__':
    print("--- WEBSITE STARTING ---")
    print("Harold, please open your browser and type this address: http://127.0.0.1:5000")
    print("-------------------------")
    app.run(debug=True)