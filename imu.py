import smbus
from imusensor.MPU9250 import MPU9250


class Imu():
    def __init__(self):
        address = 0x68
        bus = smbus.SMBus(1)
        self.imu = MPU9250.MPU9250(bus, address)
        self.imu.begin()