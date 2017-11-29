import threading

class LightControl():

    def __init__(self, p):
        self.p = p
        self.power = 0

    def printPower(self):
        print(self.power)

    def bumpPower(self):
        self.power = self.power + 50 if self.power < 50 else 100

    def drainPower(self):
        self.power = self.power - 1 if self.power > 1 else self.power

    def tick(self):
        timer = threading.Timer(0.01, self.tock)
        timer.start()
        if self.power > 1:
            self.p.ChangeDutyCycle(self.power)

    def tock(self):
        self.drainPower()
        self.tick()
