from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController
from mechanics.websocket_controller import websocket_controller

config = open("steering.config", "r")
steeringrange = config.readline().split(',')
throttlerange = config.readline().split(',')

steering = SteeringController(int(steeringrange[0]), int(steeringrange[1]))
throttle = ThrottleController(int(throttlerange[0]), int(throttlerange[1]), int(throttlerange[2]))

controller = websocket_controller()

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
    controller.start_connection(callback)
    controller.event_loop()
finally:
    steering.steer(0)
    throttle.kill_throttle()
