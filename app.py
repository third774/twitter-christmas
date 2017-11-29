import os
import time
import threading
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from LightControl import LightControl

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Pull Twitter application authentication keys from env variables
APP_KEY = os.environ.get('APP_KEY')
APP_SECRET = os.environ.get('APP_SECRET')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')

# Setup GPIO as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT) # The pin number your relay is connected to (not the GPIO number).

p = GPIO.PWM(4, 200)
p.start(0)

# Enter the hashtag you want to monitor
TERMS = '#Christmas'

class BlinkyStreamer(TwythonStreamer):
    def __init__(self, a, b, c, d, lightControl):
        TwythonStreamer.__init__(self, a, b, c, d)
        self.lightControl = lightControl 
        lightControl.tick()

    def on_success(self, data):
        if 'text' in data:
            self.lightControl.bumpPower()
            print(data['text'].encode('utf-8'))
            print("\n")

try:
    lightControl = LightControl(p)
    stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, lightControl)
    stream.statuses.filter(track=TERMS)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
