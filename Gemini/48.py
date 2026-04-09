import os
import boto3
import unittest
from flask import Flask, render_template_string, Response, request, redirect, url_for
from botocore.exceptions import NoCredentialsError, ClientError


S3_BUCKET = os.environ.get('S3_BUCKET_NAME', 'bristol-video-storage')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-2') 

app = Flask(__name__)


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


INDEX_HTML = 

WATCH_HTML = 

@app.route('/')
def index():
    
    videos = []
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        if 'Contents' in response:
            videos = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.mp4')]
    except (NoCredentialsError, ClientError) as e:
        print(f"AWS Error: {e}")
    
    return render_template_string(INDEX_HTML, videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    
    if 'video_file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['video_file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        try:
            s3_client.upload_fileobj(
                file, 
                S3_BUCKET, 
                file.filename,
                ExtraArgs={'ContentType': 'video/mp4'}
            )
        except ClientError as e:
            print(f"Upload failed: {e}")
            
    return redirect(url_for('index'))

@app.route('/watch/<video_name>')
def watch(video_name):
    
    return render_template_string(WATCH_HTML, video_name=video_name)

@app.route('/stream/<video_name>')
def stream_video(video_name):
    
    def generate():
        try:
            response = s3_client.get_object(Bucket=S3_BUCKET, Key=video_name)
            
            for chunk in response['Body'].iter_chunks(chunk_size=1024*1024):
                yield chunk
        except ClientError as e:
            print(f"Streaming error: {e}")

    return Response(generate(), mimetype='video/mp4')


class TestVideoSite(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage_load(self):
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_watch_page_context(self):
        
        test_video = "test_movie.mp4"
        response = self.client.get(f'/watch/{test_video}')
        self.assertIn(test_video.encode(), response.data)

if __name__ == '__main__':
    
    
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=[sys.argv[0]])
    else:
        
        app.run(host='0.0.0.0', port=5000, debug=True)