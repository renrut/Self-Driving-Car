from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController
from mechanics.websocket_controller import websocket_controller

config = open("steering.config", "r")
steeringrange = config.readline().split(',')
throttlerange = config.readline().split(',')

throttle = ThrottleController(throttlerange[0], throttlerange[1], throttlerange[2])
steering = SteeringController(steeringrange[0], steeringrange[1])
controller = websocket_controller()

async def callback(websocket, path):
    try:
        while True:
            datastr = await websocket.recv()
            data = datastr.split(',')
            turn = float(data[0])
            speed = float(data[1])
            steering.steer(turn)
            throttle.set_throttle(speed)
    except:
        throttle.set_throttle(0)
        steering.steer(0)

try:
    controller.start_connection(callback)
    controller.event_loop()
finally:
    steering.steer(0)
    throttle.kill_throttle()
