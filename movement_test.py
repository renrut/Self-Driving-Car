from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController

throttle = ThrottleController(0, 100)
steering = SteeringController()
key = ''

while True:
    key = input()
    if key is 'w':
        throttle.set_throttle(.50)
    if key is 'a':
        steering.steer(-.75)
    if key is 'd':
        steering.steer(.75)
    if key is 's':
        throttle.set_throttle(0)
