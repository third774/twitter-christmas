import threading

class LightControl():

    def __init__(self, p, p2):
        self.p = p
        self.p2 = p2
        self.power = 0

    def printPower(self):
        print(self.power)

    def bumpPower(self):
        self.power = self.power + 50 if self.power < 50 else 100
        self.updateDutyCycle()

    def updateDutyCycle(self):
        if self.power > 5:
            self.p.ChangeDutyCycle(self.power)
            self.p2.ChangeDutyCycle(self.power)

    def drainPower(self):
        self.power = self.power - 1 if self.power > 5 else self.power

    def tick(self):
        timer = threading.Timer(0.01, self.tock)
        timer.start()

    def tock(self):
        self.drainPower()
        self.updateDutyCycle()
        self.tick()
