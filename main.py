from gpiozero import LED, Button
from ble_gpio import BLE
from time import sleep
import asyncio

# LED Output pin
led = LED(16)

# Initial state
led_on = False

# Button
btn = Button(25, pull_up=True)

ble = BLE()

def btn_callback():
    asyncio.run(ble.start_measurement(5))

btn.when_pressed = btn_callback

if __name__ == "__main__":

    while True:
        sleep(1)
        print("Awaiting command..")