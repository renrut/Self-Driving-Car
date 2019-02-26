from mechanics.servo_controller import ServoController

class SteeringController:
    LEFT = -1
    RIGHT = 1
    CHANNEL = 0

    def __init__(self, leftvalue=290, rightvalue=490):
        self.leftvalue = leftvalue
        self.rightvalue = rightvalue
        self.servoController = ServoController(self.CHANNEL)

    # Takes a steer value between LEFT and RIGHT and calculates it to the PWM
    def calculate_steering(self, steervalue):
        difference = self.rightvalue - self.leftvalue
        midpoint = self.leftvalue + difference/2
        return midpoint + (steervalue * difference/2)

    def steer(self, steervalue):
        pwmVal = self.calculate_steering(steervalue)
        self.servoController.set_pwm(pwmVal)
