from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController
from mechanics.websocket_controller import websocket_controller

throttle = ThrottleController()
steering = SteeringController()
controller = websocket_controller()
key = ''


async def callback(websocket, path):
    name = await websocket.recv()
    key = name[-1]

try:
    controller.start_connection(callback)
    while True:
        #key = input()
        if key is 'w':
            throttle.set_throttle(.50)
        if key is 'a':
            steering.steer(-.75)
        if key is 'd':
            steering.steer(.75)
        if key is 's':
            throttle.set_throttle(0)
            steering.steer(0)
finally:
    steering.steer(0)
    throttle.set_throttle(0)
