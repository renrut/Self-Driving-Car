from mechanics.servo_controller import ServoController

class SteeringController:
    LEFT = -1
    RIGHT = 1
    CHANNEL = 1

    def __init__(self, leftvalue=290, rightvalue=490):
        self.leftvalue = leftvalue
        self.rightvalue = rightvalue
        self.servoController = ServoController(self.CHANNEL)

    # Takes a steer value between LEFT and RIGHT and calculates it to the PWM
    def calculate_steering(self, steervalue):
        difference = self.rightvalue - self.leftvalue
        midpoint = self.leftvalue + difference/2
        return int(midpoint + (steervalue * difference/2))

    def steer(self, steervalue):
        pwm_val = self.calculate_steering(steervalue)
        print("Setting steering to " + str(pwm_val))
        self.servoController.set_pwm(pwm_val)
