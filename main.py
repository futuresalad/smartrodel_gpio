from gpiozero import Button
from ble_gpio import BLE
from time import sleep
import asyncio

# Button
btn = Button(16, pull_up=True)

ble = BLE()

def btn_callback():
    print("Button pressed")
    for s in range(3):
        ble.led_r.on()
        sleep(1)
        ble.led_r.off()
        sleep(1)
        
    asyncio.run(ble.start_measurement(60))
        
btn.when_pressed = btn_callback

if __name__ == "__main__":
    print("Awaiting command..")
    
    while True:
        sleep(1)
        