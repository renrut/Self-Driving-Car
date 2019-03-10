from mechanics.servo_controller import ServoController


class ThrottleController:
    OFF = 0
    FULL = 1
    CHANNEL = 2
    controller = None

    def __init__(self, zero_pulse=350, max_pulse=250, min_pulse=490):
        self.zero_pulse = zero_pulse
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.servoController = ServoController(self.CHANNEL)
        self.servoController.set_pwm(self.zero_pulse)

    # Takes a throttle value between OFF and FULL and calculates it to the PWM
    def calculate_throttle(self, throttle):
        difference = self.zero_pulse - self.max_pulse
        return int(self.zero_pulse - (difference * throttle))

    def set_throttle(self, throttlevalue):
        pwmval = self.calculate_throttle(throttlevalue)
        print("Mapped " + str(throttlevalue) + " to " + str(pwmval))
        self.servoController.set_pwm(pwmval)

    def kill_throttle(self):
        self.set_throttle(0)
