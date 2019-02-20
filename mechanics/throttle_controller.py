from .servo_controller import ServoController


class ThrottleController:
    OFF = 0
    FULL = 1
    CHANNEL = 1

    def __init__(self, offvalue, fullvalue):
        self.offvalue = offvalue
        self.fullvalue = fullvalue
        self.servoController = ServoController(self.CHANNEL)

    # Takes a steer value between OFF and FULL and calculates it to the PWM
    def calculate_steering(self, throttle):
        difference = self.fullvalue - self.offvalue
        return self.offvalue + (difference * throttle)

    def set_throttle(self, steervalue):
        pwmval = self.calculateSteering(steervalue)
        self.servoController.set_pwm(pwmval)

    def kill_throttle(self):
        self.set_throttle(0)
