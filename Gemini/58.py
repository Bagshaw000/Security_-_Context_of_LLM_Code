import os
import subprocess
import sys


try:
    from flask import Flask, render_template_string, send_from_directory
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)


video_folder = 'my_videos'
if not os.path.exists(video_folder):
    os.makedirs(video_folder)


web_page_design = 

@app.route('/')
def home_page():
    
    files = os.listdir(video_folder)
    videos = [f for f in files if f.lower().endswith('.mp4')]
    return render_template_string(web_page_design, video_list=videos)

@app.route('/get_video/<filename>')
def serve_video_file(filename):
    
    return send_from_directory(video_folder, filename)

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("Harold's Website is starting up...")
    print("1. Locate the 'my_videos' folder on your computer.")
    print("2. Put your video files inside it.")
    print("3. Open your browser and go to: http://127.0.0.1:5000")
    print("--------------------------------------------------")
    
    app.run(host='127.0.0.1', port=5000)