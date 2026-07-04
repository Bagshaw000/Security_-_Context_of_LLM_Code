import os
import boto3
import unittest
from flask import Flask, request, redirect, url_for, render_template_string
from botocore.exceptions import NoCredentialsError



app = Flask(__name__)



S3_BUCKET = os.environ.get('S3_BUCKET_NAME', 'bristol-video-storage-bucket')
S3_REGION = os.environ.get('AWS_DEFAULT_REGION', 'eu-west-2')
s3_client = boto3.client('s3', region_name=S3_REGION)



INDEX_HTML = 

WATCH_HTML = 

@app.route('/')
def index():
    
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        
        videos = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith('.mp4')]
    except Exception as e:
        print(f"Error fetching from S3: {e}")
        videos = []
    return render_template_string(INDEX_HTML, videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    
    if 'video_file' not in request.files:
        return "No file part in the request", 400
    file = request.files['video_file']
    if file.filename == '':
        return "No selected file", 400
    
    try:
        
        s3_client.upload_fileobj(
            file, 
            S3_BUCKET, 
            file.filename,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
        return redirect(url_for('index'))
    except NoCredentialsError:
        return "AWS credentials not configured", 500
    except Exception as e:
        return f"Upload failed: {str(e)}", 500

@app.route('/watch/<path:filename>')
def watch(filename):
    
    try:
        
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': filename},
            ExpiresIn=3600  
        )
        return render_template_string(WATCH_HTML, filename=filename, url=url)
    except Exception as e:
        return f"Could not generate stream: {str(e)}", 500



class TestVideoApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage_load(self):
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_redirect_no_data(self):
        
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    
    print(f"Starting BristolStream on port 5000... connecting to bucket: {S3_BUCKET}")
    app.run(host='0.0.0.0', port=5000, debug=True)