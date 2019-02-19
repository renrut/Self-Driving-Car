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
    def calculateSteering(self, throttle):
        difference = self.fullvalue - self.offvalue
        return self.offvalue + (self.offvalue * difference)

    def setThrottle(self, steerValue):
        pwmVal = self.calculateSteering(steerValue)
        self.servoController.set_pwm(pwmVal)

    def killThrottle(self):
        self.setThrottle(0)
