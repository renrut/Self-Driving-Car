from .servo_controller import ServoController


class SteeringController:
    LEFT = -1
    RIGHT = 1
    CHANNEL = 0

    def __init__(self, leftValue=290, rightValue=490):
        self.leftValue = leftValue
        self.rightValue = rightValue
        self.servoController = ServoController(self.CHANNEL)

    # Takes a steer value between LEFT and RIGHT and calculates it to the PWM
    def calculateSteering(self, steerValue):
        difference = self.rightValue - self.leftValue
        midpoint = self.leftValue + difference/2
        return midpoint + (steerValue * difference/2)

    def steer(self, steerValue):
        pwmVal = self.calculateSteering(steerValue)
        self.servoController.set_pwm(pwmVal)
