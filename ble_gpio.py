from time import sleep
import asyncio
from bleak import BleakClient
import pandas as pd
import numpy as np
import datetime
import asyncio

class BLE():
    def __init__(self):
         
        # BLE Device constants
        self.mac = "24:0A:C4:62:52:FE" #dev nxn
        self.RX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
        self.TX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

        # BLE status
        self.connected = False

        # Commands
        self.txOn = bytearray("on",'utf-8')
        self.txOff = bytearray("off",'utf-8')

        # Dataframe to save measurements
        self.rec = np.zeros([1,5])
        self.dataframe = pd.DataFrame(self.rec, columns=['time', 'vl', 'vr', 'hl', 'hr'])

    def bt_callback(self, sender: int, data: bytearray):
        # Decode data from bytearrays to strings and split them at the "," delimiter
        self.rec = data.decode("utf-8").split(",")
        print(self.rec)
        # Convert every element of the row into an integer
        for idx, element in enumerate(self.rec):
            self.rec[idx] = int(element)

        # Add that array as a row to the dataframe
        self.dataframe.loc[len(self.dataframe)] = self.rec


    def export_data(self):
            print("Exporting CSV")
            self.dataframe.to_csv(path_or_buf=f"./data_export/data_{datetime.datetime.now().isoformat()}.csv", sep=',', index_label="Index", na_rep='NaN')

    async def start_measurement(self, duration):

        self.rec = np.zeros([1,5])
        self.dataframe = pd.DataFrame(self.rec, columns=['time', 'vl', 'vr', 'hl', 'hr'])

        try:
            async with BleakClient(self.mac) as client:
                    
                if client.is_connected:
                        
                        await client.start_notify(self.RX_UUID, self.bt_callback)
                        await client.write_gatt_char(self.TX_UUID, bytearray(str(duration),'utf-8'))
                        await client.write_gatt_char(self.TX_UUID, self.txOn)
                        sleep(duration)
                        await client.write_gatt_char(self.TX_UUID, self.txOff)
                        await client.disconnect()
                        self.success = True
                        
                        
                else:
                    print(f'BT Device with MAC {self.mac} not found')    

        except Exception as e:

            print(e)
            self.success = False
                    
        if self.success:
            self.export_data()
            print("Success!")

        else:
            print("not successful")
