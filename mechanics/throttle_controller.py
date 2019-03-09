from mechanics.servo_controller import ServoController


class ThrottleController:
    OFF = 0
    FULL = 1
    CHANNEL = 0
    controller = None
    max_pulse = 300
    min_pulse = 490
    zero_pulse = 350

    def __init__(self, offvalue, fullvalue):
        self.offvalue = offvalue
        self.fullvalue = fullvalue
        self.servoController = ServoController(self.CHANNEL)
        self.servoController.set_pwm(self.zero_pulse)

    # Takes a steer value between OFF and FULL and calculates it to the PWM
    def calculate_steering(self, throttle):
        difference = self.max_pulse - self.min_pulse
        return int(self.min_pulse + (difference * throttle))

    def set_throttle(self, steervalue):
        pwmval = self.calculate_steering(steervalue)
        print("Setting steering to " + str(pwmval))
        self.servoController.set_pwm(pwmval)

    def kill_throttle(self):
        self.set_throttle(0)
