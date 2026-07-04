import os
import re
import unittest
from flask import Flask, send_file, request, Response, render_template_string



app = Flask(__name__)




HTML_TEMPLATE = 

@app.route('/')
def home():
    
    return render_template_string(HTML_TEMPLATE)

def get_video_chunk(path, start, end=None):
    
    file_size = os.path.getsize(path)
    if end is None:
        end = file_size - 1
    
    length = end - start + 1
    with open(path, 'rb') as f:
        f.seek(start)
        data = f.read(length)
    return data, start, end, file_size

@app.route('/stream/<filename>')
def stream_video(filename):
    
    video_path = os.path.join('static', 'videos', filename)
    
    if not os.path.exists(video_path):
        return "Video Asset Not Found", 404

    range_header = request.headers.get('Range', None)
    if not range_header:
        
        return send_file(video_path)

    
    byte_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
    start_byte = int(byte_match.group(1))
    end_byte = byte_match.group(2)
    end_byte = int(end_byte) if end_byte else None

    chunk, start, end, total = get_video_chunk(video_path, start_byte, end_byte)

    response = Response(
        chunk, 
        206, 
        mimetype='video/mp4', 
        content_type='video/mp4',
        direct_passthrough=True
    )
    response.headers.add('Content-Range', f'bytes {start}-{end}/{total}')
    response.headers.add('Accept-Ranges', 'bytes')
    return response

class TestVideoSite(unittest.TestCase):
    
    
    def setUp(self):
        self.app = app.test_client()
        
        if not os.path.exists('static/videos'):
            os.makedirs('static/videos', exist_ok=True)

    def test_homepage_load(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Video Streamer', response.data)

    def test_invalid_video_returns_404(self):
        response = self.app.get('/stream/non_existent.mp4')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    
    
    print("Starting video streaming server...")
    app.run(host='0.0.0.0', port=5000, debug=True)