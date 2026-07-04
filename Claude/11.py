Here's the Python code to create a video streaming website:

from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/videos'

@app.route('/')
def index():
    videos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/watch/<filename>')
def watch(filename):
    return render_template('watch.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)