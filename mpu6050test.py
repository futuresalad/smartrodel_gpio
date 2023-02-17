import time
from mpu6050 import mpu6050
sensor = mpu6050(0x68)

#tick = time.time()
#data1 = sensor.get_gyro_data()
#dur1 = time.time() - tick
#
#tick = time.time()
#data2 = sensor.get_accel_data()
#dur2 = time.time() - tick
#
#tick = time.time()
#data3 = sensor.get_all_data()
#dur3 = time.time() - tick
#print(f'Gyro: {data1} t: {dur1} \n Accel: {data2} t: {dur2} \n All: {data3} t: {dur3}')

data_big = []
samplerate = 50
sampletime = 1/samplerate

start = time.time()
lastread = 0

tick = time.time()

while True:
    
    dt =  time.time() - start
    

    if (lastread < (dt+sampletime)):
        lastread = time.time() - start
        #print(lastread)
        data1 = sensor.get_gyro_data()
        data2 = sensor.get_accel_data()
        data_big.append([data1['x'],data1['y'],data1['z'],data2['x'],data2['y'],data2['z']])
    
    if len(data_big) > 500:
        break

tock = time.time()



print(f'duration: {tock-tick}')

