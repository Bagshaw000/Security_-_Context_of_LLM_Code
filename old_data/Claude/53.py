import os
from flask import Flask, render_template, request, redirect, url_for, flash
import cv2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    filename = file.filename
    file.save(os.path.join('static', filename))
    flash('Video uploaded successfully!')
    return redirect(url_for('stream'))

@app.route('/play/<filename>')
def play(filename):
    video_path = os.path.join('static', filename)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    return render_template('play.html', video_path=video_path, fps=fps)

if __name__ == '__main__':
    app.run(debug=True)