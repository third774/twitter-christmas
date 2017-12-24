import os
import time
import threading
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from dotenv import load_dotenv, find_dotenv

from LightControl import LightControl

# Setup GPIO as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT) # The pin number your relay is connected to (not the GPIO number).
GPIO.setup(17, GPIO.OUT)

p = GPIO.PWM(4, 100)
p.start(100)
p2 = GPIO.PWM(17, 100)
p2.start(100)


load_dotenv(find_dotenv())

# Pull Twitter application authentication keys from env variables
APP_KEY = os.environ.get('APP_KEY')
APP_SECRET = os.environ.get('APP_SECRET')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')


# Enter the hashtag you want to monitor
TERMS = '#Christmas'

class BlinkyStreamer(TwythonStreamer):
    def __init__(self, a, b, c, d, lightControl):
        TwythonStreamer.__init__(self, a, b, c, d)
        self.lightControl = lightControl 
        lightControl.tick()

    def on_success(self, data):
        self.lightControl.bumpPower()

    def on_error(self, status_code, data):
        print(status_code)


lightControl = LightControl(p, p2)
stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, lightControl)

running = True
while running:
    try:
        print('starting')
        stream.statuses.filter(track=TERMS)
    except KeyboardInterrupt:
        print('exiting')
        p.stop()
        p2.stop()
        GPIO.cleanup()
        running = False
    except:
        print('error')
        continue
