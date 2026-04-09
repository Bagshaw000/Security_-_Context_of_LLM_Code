








import os
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)


VIDEO_DIRECTORY = "videos"


if not os.path.exists(VIDEO_DIRECTORY):
    os.makedirs(VIDEO_DIRECTORY)


HTML_LAYOUT = 

@app.route('/')
def home_page():
    
    all_files = os.listdir(VIDEO_DIRECTORY)
    videos = [f for f in all_files if f.lower().endswith('.mp4')]
    return render_template_string(HTML_LAYOUT, video_list=videos, playing_now=None)

@app.route('/watch/<filename>')
def watch_page(filename):
    
    return render_template_string(HTML_LAYOUT, playing_now=filename)

@app.route('/video_data/<filename>')
def get_video_file(filename):
    
    return send_from_directory(VIDEO_DIRECTORY, filename)

if __name__ == '__main__':
    print("--- Website is starting! ---")
    print("Step 1: Open your web browser.")
    print("Step 2: Go to http://127.0.0.1:5000")
    print("Step 3: To stop the website, press Ctrl and C at the same time in this window.")
    app.run(debug=True)