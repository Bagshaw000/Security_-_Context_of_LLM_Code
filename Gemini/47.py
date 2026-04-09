import os
import boto3
import unittest
from flask import Flask, Response, render_template_string, request, stream_with_context
from botocore.exceptions import NoCredentialsError, ClientError
from unittest.mock import MagicMock, patch

app = Flask(__name__)



S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'bristol-video-archive-2023')
S3_REGION = os.environ.get('AWS_DEFAULT_REGION', 'eu-west-2')

s3_client = boto3.client('s3', region_name=S3_REGION)


INDEX_TEMPLATE = 

WATCH_TEMPLATE = 

@app.route('/')
def index():
    
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
        files = response.get('Contents', [])
        video_files = [f['Key'] for f in files if f['Key'].lower().endswith('.mp4')]
        return render_template_string(INDEX_TEMPLATE, videos=video_files, bucket=S3_BUCKET_NAME)
    except (NoCredentialsError, ClientError) as e:
        return f"AWS Configuration Error: {str(e)}", 500
    except Exception as e:
        return f"Server Error: {str(e)}", 500

@app.route('/watch/<path:filename>')
def watch(filename):
    
    return render_template_string(WATCH_TEMPLATE, filename=filename)

@app.route('/video_feed/<path:filename>')
def video_feed(filename):
    
    def generate():
        try:
            s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=filename)
            
            for chunk in s3_object['Body'].iter_chunks(chunk_size=1024 * 1024):
                yield chunk
        except ClientError as e:
            app.logger.error(f"S3 Retrieval Error: {e}")

    return Response(stream_with_context(generate()), mimetype='video/mp4')




class TestVideoSite(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('boto3.client')
    def test_index_lists_videos(self, mock_s3):
        
        mock_instance = MagicMock()
        mock_instance.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'presentation.mp4'},
                {'Key': 'tutorial.mp4'},
                {'Key': 'image.jpg'}
            ]
        }
        
        with patch('__main__.s3_client', mock_instance):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'presentation.mp4', response.data)
            self.assertIn(b'tutorial.mp4', response.data)
            self.assertNotIn(b'image.jpg', response.data)

    def test_watch_page_loads(self):
        response = self.client.get('/watch/test_video.mp4')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_video.mp4', response.data)

    @patch('boto3.client')
    def test_streaming_response(self, mock_s3):
        mock_instance = MagicMock()
        
        mock_body = MagicMock()
        mock_body.iter_chunks.return_value = [b'chunk1', b'chunk2']
        mock_instance.get_object.return_value = {'Body': mock_body}

        with patch('__main__.s3_client', mock_instance):
            response = self.client.get('/video_feed/test.mp4')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'video/mp4')
            self.assertEqual(response.data, b'chunk1chunk2')

def run_tests():
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVideoSite)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    
    if os.environ.get('RUN_TESTS'):
        run_tests()
    else:
        
        
        print("Starting Video Streaming Service...")
        app.run(host='0.0.0.0', port=5000, debug=True)