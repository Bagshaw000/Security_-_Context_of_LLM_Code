from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

AWS_ACCESS_KEY_ID = 'your_aws_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_aws_secret_access_key'
BUCKET_NAME = 'your_s3_bucket_name'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    videos = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                s3.upload_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), BUCKET_NAME, filename)
                print(f'Successfully Uploaded {filename} to S3 Bucket')
            except NoCredentialsError:
                print('AWS credentials not available')
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/watch/<filename>')
def watch_video(filename):
    return render_template('watch.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)