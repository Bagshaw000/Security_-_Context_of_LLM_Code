import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 8000

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)

        if parsed_path.path == '/stream':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello from server')
        elif parsed_path.path == '/video.mp4':
            self.send_response(200)
            self.end_headers()
            with open('video.mp4', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

server = socketserver.TCPServer(('localhost', PORT), RequestHandler)
http.server.HTTPServer.http_server_class = server
server.serve_forever()