import os
import boto3
import unittest
from flask import Flask, render_template_string, request, redirect, url_for
from botocore.exceptions import NoCredentialsError


app = Flask(__name__)



S3_BUCKET = os.environ.get('S3_BUCKET_NAME', 'bristol-video-storage')
S3_REGION = os.environ.get('AWS_REGION', 'eu-west-2')
s3_client = boto3.client('s3', region_name=S3_REGION)


INDEX_HTML = 

WATCH_HTML = 

@app.route('/')
def index():
    
    videos = []
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        if 'Contents' in response:
            videos = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.mp4')]
    except Exception as e:
        print(f"Error fetching from S3: {e}")
    
    return render_template_string(INDEX_HTML, videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    
    file = request.files.get('video_file')
    if file and file.filename != '':
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
    
    try:
        
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': filename},
            ExpiresIn=3600
        )
    except Exception as e:
        return str(e), 500
        
    return render_template_string(WATCH_HTML, filename=filename, video_url=url)



class TestStreamingApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_route(self):
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Video Management System', response.data)

    def test_upload_redirect(self):
        
        response = self.client.post('/upload', data={'video_file': (None, '')})
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    
    
    app.run(host='0.0.0.0', port=5000, debug=True)