from gpiozero import Button
from ble_gpio import BLE
from time import sleep
import asyncio

# Button
btn = Button(16, pull_up=True)

ble = BLE()

def btn_callback():
    asyncio.run(ble.start_measurement(60))

btn.when_pressed = btn_callback

if __name__ == "__main__":

    while True:
        sleep(1)
        print("Awaiting command..")