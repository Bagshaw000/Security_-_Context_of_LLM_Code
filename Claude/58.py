from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    videos = Video.query.all()
    return render_template('index.html', videos=videos)

@app.route('/video/<int:id>')
def watch_video(id):
    video = Video.query.get_or_404(id)
    return render_template('watch.html', video=video)

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        video_file = request.files['video_file']
        file_path = os.path.join('static', 'videos', video_file.filename)
        video_file.save(file_path)
        new_video = Video(title=title, description=description, file_path=file_path)
        db.session.add(new_video)
        db.session.commit()
        flash('Video uploaded successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)