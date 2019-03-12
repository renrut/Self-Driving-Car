import logging
import socketserver
from http import server
from mechanics.camera_controller import CameraController
from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController
from mechanics.websocket_controller import websocket_controller

config = open("config/steering.config", "r")
steeringrange = config.readline().split(',')
throttlerange = config.readline().split(',')

steering = SteeringController(int(steeringrange[0]), int(steeringrange[1]))
throttle = ThrottleController(int(throttlerange[0]), int(throttlerange[1]), int(throttlerange[2]))

camera = CameraController()

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
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                output = camera.get_streaming_output()
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

async def callback(websocket, path):
    try:
        while True:
            datastr = await websocket.recv()
            if datastr.startswith("drive "):
                datastr = datastr.replace("drive ", "")
                data = datastr.split(',')
                turn = float(data[0])
                speed = float(data[1])
                steering.steer(turn)
                throttle.set_throttle(speed)
            elif datastr.startswith("record"):
                print("recording")
            elif datastr.startswith("stop"):
                print("stopping recording")


    except:
        throttle.set_throttle(0)
        steering.steer(0)

try:
    camera.start()
    controller = websocket_controller()
    controller.start_connection(callback)
    controller.event_loop()
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler, camera)
    server.serve_forever()

finally:
    steering.steer(0)
    throttle.kill_throttle()
    camera.stop()
