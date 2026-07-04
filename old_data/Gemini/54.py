import os
import re
from flask import Flask, request, Response, stream_with_context

class VideoMetadata:
    def __init__(self, video_id, title, file_path):
        self.video_id = video_id
        self.title = title
        self.file_path = file_path

class DeviceIdentityManager:
    
    def validate_session(self, auth_token):
        
        return True

class VideoStreamEngine:
    def __init__(self, buffer_size=1024 * 1024):
        self.buffer_size = buffer_size

    def get_range_params(self, range_header, file_size):
        if not range_header:
            return 0, file_size - 1
        
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        if not match:
            return 0, file_size - 1

        start = int(match.group(1))
        end = match.group(2)
        end = int(end) if end else file_size - 1
        return start, end

    def stream_video(self, path, start, end, file_size):
        with open(path, 'rb') as video_file:
            video_file.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk_size = min(self.buffer_size, remaining)
                data = video_file.read(chunk_size)
                if not data:
                    break
                yield data
                remaining -= len(data)

class VideoStreamingApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.stream_engine = VideoStreamEngine()
        self.identity_manager = DeviceIdentityManager()
        
        self.video_catalog = {
            "vid123": VideoMetadata("vid123", "System Architecture Deep Dive", "assets/video1.mp4")
        }
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return {"status": "healthy", "service": "video-streaming-v1"}, 200

        @self.app.route('/v1/stream/<video_id>', methods=['GET'])
        def stream(video_id):
            
            token = request.headers.get('Authorization')
            if not self.identity_manager.validate_session(token):
                return Response("Unauthorized Device", status=401)

            video = self.video_catalog.get(video_id)
            if not video or not os.path.exists(video.file_path):
                return Response("Video Not Found", status=404)

            file_size = os.path.getsize(video.file_path)
            range_header = request.headers.get('Range', None)
            start, end = self.stream_engine.get_range_params(range_header, file_size)

            
            if start >= file_size or end >= file_size:
                return Response("Requested Range Not Satisfiable", status=416)

            response_body = self.stream_engine.stream_video(video.file_path, start, end, file_size)
            
            headers = {
                'Content-Range': f'bytes {start}-{end}/{file_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(end - start + 1),
                'Content-Type': 'video/mp4',
            }

            return Response(
                stream_with_context(response_body),
                status=206,
                headers=headers,
                direct_passthrough=True
            )

    def run(self, host='0.0.0.0', port=8080):
        
        self.app.run(host=host, port=port, threaded=True)

if __name__ == "__main__":
    
    if not os.path.exists('assets'):
        os.makedirs('assets')
        
    streaming_service = VideoStreamingApp()
    