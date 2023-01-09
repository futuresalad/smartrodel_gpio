from gpiozero import LED, Button

from time import sleep
import asyncio
from bleak import BleakClient
import pandas as pd
import numpy as np
import datetime
import asyncio

# BLE Device constants
mac = "24:0A:C4:62:52:FE" #dev nxn
RX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
TX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

# BLE status
connected = False

# Commands
txOn = bytearray("on",'utf-8')
txOff = bytearray("off",'utf-8')

# Dataframe to save measurements
rec = np.zeros([1,5])
dataframe = pd.DataFrame(rec, columns=['time', 'vl', 'vr', 'hl', 'hr'])


# LED Output pin
led = LED(16)

# Initial state
led_on = False

# Button
btn = Button(25, pull_up=True)


def bt_callback(sender: int, data: bytearray):
    # Decode data from bytearrays to strings and split them at the "," delimiter
    rec = data.decode("utf-8").split(",")
    print(rec)
    # Convert every element of the row into an integer
    for idx, element in enumerate(rec):
        rec[idx] = int(element)

    # Add that array as a row to the dataframe
    dataframe.loc[len(dataframe)] = rec


def export_data():
        print("Exporting CSV")
        dataframe.to_csv(path_or_buf=f"./data_export/data_{datetime.datetime.now().isoformat()}.csv", sep=',', index_label="Index", na_rep='NaN')

async def start_measurement(duration):

    rec = np.zeros([1,5])
    dataframe = pd.DataFrame(rec, columns=['time', 'vl', 'vr', 'hl', 'hr'])

    try:
        async with BleakClient(mac) as client:
                
            if client.is_connected:
                    led.on()
                    await client.start_notify(RX_UUID, bt_callback)
                
                    await client.write_gatt_char(TX_UUID, bytearray(str(duration),'utf-8'))
                    await client.write_gatt_char(TX_UUID, txOn)
                    sleep(duration)
                    await client.write_gatt_char(TX_UUID, txOff)
                    client.disconnect()
                    print(f"Client connected: {client.is_connected()}")
                    success = True
                    led.off()
                    
            else:
                print(f'BT Device with MAC {mac} not found')    

    except Exception as e:

        print(e)
        success = False
                   
    if success:
        export_data()
        print("Success!")

    else:
        print("not successful")


btn.when_pressed = asyncio.run(start_measurement(5))

if __name__ == "__main__":

    while True:
        sleep(1)
        print("Awaiting command..")