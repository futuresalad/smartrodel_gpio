import RPi.GPIO as GPIO
from time import sleep
from ble import bt_daq
import asyncio

# BLE Device constants
mac = "24:0A:C4:62:52:FE" #dev nxn

# BLE status
connected = False

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

def callback(ev=None):

    for i in range(5):
        GPIO.output(led_pin, GPIO.HIGH)
        sleep(.1)
        GPIO.output(led_pin, GPIO.LOW)
        sleep(.1)

    global led_on
    led_on = not led_on
    GPIO.output(led_pin, GPIO.HIGH if led_on else GPIO.LOW)
    asyncio.run(start_measurement())


async def start_measurement():
            success = await ESP32_1.get_data(2)

            if success:
                ESP32_1.export_data()

                for i in range(5):
                    GPIO.output(led_pin, GPIO.HIGH)
                    sleep(.5)
                    GPIO.output(led_pin, GPIO.LOW)
                    sleep(.1)

            else:
                print("not successful")

                for i in range(3):

                    GPIO.output(led_pin, GPIO.HIGH)
                    sleep(1)
                    GPIO.output(led_pin, GPIO.LOW)
                    sleep(1)

ESP32_1 = bt_daq(mac)
GPIO.add_event_detect(btn_pin, GPIO.RISING, callback=callback, bouncetime=300)

if __name__ == "__main__":

    while True:
        sleep(5)
        print("Awaiting Start..")