import socketserver
from http import server


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            f = open('./web/frontpage.html', 'rb')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        elif self.path.startswith('/js') or self.path.startswith('/css'):
            #serving assets
            f = open('./web' + self.path, 'rb')
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class WebServer:
    PORT = 8000

    def run(self):
        print("Listening on port " + str(self.PORT))
        self.address = ('', self.PORT)
        self.server = StreamingServer(self.address, StreamingHandler)
        self.server.serve_forever()
