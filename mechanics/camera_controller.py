import picamera
import io
from threading import Condition


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class CameraController:
    def __init__(self, resolution='640x480', framerate=24):
        self.resolution = resolution
        self.framerate = framerate
        self.output = StreamingOutput()
        self.camera = picamera.PiCamera(resolution=self.resolution, framerate=self.framerate)


    def start(self):
        self.camera.start_recording(self.output, format='mjpeg')

    def stop(self):
        self.camera.stop_recording()

    def get_streaming_output(self):
        return self.output

    def capture_still(self, filename):
        self.camera.capture(filename, use_video_port=True)
