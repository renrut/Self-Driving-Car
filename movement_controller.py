from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController
from mechanics.websocket_controller import websocket_controller

throttle = ThrottleController()
steering = SteeringController()
controller = websocket_controller()
key = ''

def process_input(key):
    if key is 'w':
        throttle.set_throttle(.50)
    if key is 'd':
        steering.steer(-.75)
    if key is 'a':
        steering.steer(.75)
    if key is 's':
        throttle.set_throttle(-.2)
    if key is 'r':
        throttle.kill_throttle()
        steering.steer(0)



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
