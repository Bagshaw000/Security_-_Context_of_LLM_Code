from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    video_file = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    videos = Video.query.all()
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        video_file = request.files['video_file']
        new_video = Video(title=title, description=description, video_file=video_file.filename)
        db.session.add(new_video)
        db.session.commit()
        video_file.save(os.path.join('static/videos', video_file.filename))
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/video/<int:id>')
def watch_video(id):
    video = Video.query.get_or_404(id)
    return render_template('watch.html', video=video)

if __name__ == '__main__':
    app.run(debug=True)