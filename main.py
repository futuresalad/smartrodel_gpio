import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LED Output pin
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

# Initial state
led_on = False
led_pin = 16
# Button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
btn_pin = 25

for i in range(5):
    GPIO.output(led_pin, GPIO.HIGH)
    sleep(.1)
    GPIO.output(led_pin, GPIO.LOW)
    sleep(.1)

def callback(ev=None):
    global led_on
    led_on = not led_on
    GPIO.output(led_pin)

GPIO.add_event_detect(23, GPIO.RISING, callback=callback, bouncetime=300)

while True:
    sleep(1)