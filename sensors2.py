import time
from mpu6050 import mpu6050
sensor = mpu6050(0x68)

data_big = []
samplerate = 50
sampletime = 1/samplerate

start = time.time()
lastread = 0
dt = 0
duration = 10

tick = time.time()

while dt <= duration:
    
    dt =  time.time() - start
    

    if (lastread < (dt+sampletime)):
        print((dt + sampletime)- lastread)
        lastread = time.time() - start
        
        try:
            data1 = sensor.get_gyro_data()
            data2 = sensor.get_accel_data()

        except Exception as e:
            print(e)
        
        finally:
            data_big.append([lastread,data1['x'],data1['y'],data1['z'],data2['x'],data2['y'],data2['z']])
    

tock = time.time()
#print(data_big)
print(f'Samples: {len(data_big)}')

