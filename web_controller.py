from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController
from mechanics.websocket_controller import websocket_controller
from mechanics.camera_controller import CameraController
import asyncio

class WebSocketController:

    def __init__(self):
        config = open("steering.config", "r")
        self.camera = CameraController()
        controllerport = 8765
        cameraport = 8766
        steeringrange = config.readline().split(',')
        throttlerange = config.readline().split(',')
        self.steering = SteeringController(int(steeringrange[0]), int(steeringrange[1]))
        self.throttle = ThrottleController(int(throttlerange[0]), int(throttlerange[1]), int(throttlerange[2]))
        self.camerasocket = websocket_controller(port=cameraport)
        self.controllersocket = websocket_controller(port=controllerport)

    async def controller_callback(self, ws, path):
        print("In controller")
        try:
            while True:
                print("waiting for event")
                datastr = await ws.recv()
                if datastr.startswith("drive "):
                    datastr = datastr.replace("drive ", "")
                    data = datastr.split(',')
                    turn = float(data[0])
                    speed = float(data[1])
                    self.steering.steer(turn)
                    self.throttle.set_throttle(speed)
                elif datastr.startswith("record"):
                    print("recording")
                elif datastr.startswith("stop"):
                    print("stopping recording")
        except:
            self.throttle.set_throttle(0)
            self.steering.steer(0)

    async def camera_callback(self, ws, path):
        print("In camera")
        try:
            output = self.camera.get_streaming_output()
            print("Got camera output")
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                    await ws.send(frame)
                    await asyncio.sleep(0.01)
        except Exception as e:
            print("exception occurred")

    def run(self):
        try:
            self.camera.start()
            self.controllersocket.start_connection(self.controller_callback)
            self.camerasocket.start_connection(self.camera_callback)
            asyncio.get_event_loop().run_forever()

        finally:
            self.steering.steer(0)
            self.throttle.kill_throttle()
            self.camera.stop()
