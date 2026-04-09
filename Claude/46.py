import flask
from flask import Flask, render_template, request, redirect, url_for, session
import os
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/videos'

class VideoUploadForm(FlaskForm):
    video_file = FileField('Upload Video')
    submit = SubmitField('Upload')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoUploadForm()
    if form.validate_on_submit():
        video_file = form.video_file.data
        filename = secure_filename(video_file.filename)
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('video_player', filename=filename))
    return render_template('index.html', form=form)

@app.route('/video/<filename>')
def video_player(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('video_player.html', video_path=video_path)

if __name__ == '__main__':
    app.run(debug=True)