from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController
from mechanics.websocket_controller import websocket_controller
from mechanics.camera_controller import CameraController
import asyncio

config = open("steering.config", "r")

camera = CameraController()

controllerport = 8765
cameraport = 8766

steeringrange = config.readline().split(',')
throttlerange = config.readline().split(',')

steering = SteeringController(int(steeringrange[0]), int(steeringrange[1]))
throttle = ThrottleController(int(throttlerange[0]), int(throttlerange[1]), int(throttlerange[2]))

controllersocket = websocket_controller(port=controllerport)
camerasocket = websocket_controller(port=cameraport)

async def controller_callback(ws, path):
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
                steering.steer(turn)
                throttle.set_throttle(speed)
            elif datastr.startswith("record"):
                print("recording")
            elif datastr.startswith("stop"):
                print("stopping recording")
    except:
        throttle.set_throttle(0)
        steering.steer(0)

async def camera_callback(ws, path):
    print("In camera")
    try:
        output = camera.get_streaming_output()
        print("Got camera output")
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                await ws.send(frame)
                await asyncio.sleep(0.01)
    except Exception as e:
        print("exception occurred")
try:
    camera.start()
    camerasocket.start_connection(camera_callback)
    controllersocket.start_connection(controller_callback)
    asyncio.get_event_loop().run_forever()

finally:
    steering.steer(0)
    throttle.kill_throttle()
    camera.stop()
