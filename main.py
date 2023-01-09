import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    if GPIO.input(5):
        print("Pin 11 is HIGH")

    else:
        print("Pin 11 is LOW")
