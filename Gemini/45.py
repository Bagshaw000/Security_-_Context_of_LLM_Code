import os
import boto3
import unittest
from flask import Flask, render_template_string, request, Response, redirect, url_for
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)


S3_BUCKET = os.environ.get('S3_BUCKET_NAME', 'bristol-video-storage')
S3_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
S3_SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_REGION = os.environ.get('AWS_REGION', 'eu-west-2')

s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name=S3_REGION
)


INDEX_HTML = 

PLAYER_HTML = 

@app.route('/')
def index():
    
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        videos = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.mp4')]
    except Exception as e:
        print(f"Error fetching from S3: {e}")
        videos = []
    return render_template_string(INDEX_HTML, videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    
    if 'video_file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['video_file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    try:
        s3_client.upload_fileobj(
            file, 
            S3_BUCKET, 
            file.filename,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
    except NoCredentialsError:
        return "AWS Credentials not found", 403
    
    return redirect(url_for('index'))

@app.route('/watch/<filename>')
def watch(filename):
    
    return render_template_string(PLAYER_HTML, filename=filename)

@app.route('/stream_source/<filename>')
def stream_source(filename):
    
    def generate():
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=filename)
        for chunk in response['Body'].iter_chunks(chunk_size=1024*1024): 
            yield chunk
            
    return Response(generate(), mimetype='video/mp4')


class VideoAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage_load(self):
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_redirect(self):
        
        response = self.client.post('/upload', data={'video_file': (None, '')})
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=[sys.argv[0]])
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)