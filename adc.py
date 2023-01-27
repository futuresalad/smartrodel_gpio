import time
import Adafruit_MCP3008 as MCP
import Adafruit_GPIO.SPI as SPI

# MCP3008 Pinout
# CH0 -|1 * 16|- VDD
# CH1 -|2   15|- Vref
# CH2 -|3   14|- AGND
# CH3 -|4   13|- CLK
# CH4 -|5   12|- Dout
# CH5 -|6   11|- Din_
# CH6 -|7   10|- CS
# CH7 -|8 __ 9|- DGND

# Raspberry Pi Pinout
# CS -> GPIO25 (Pin 22)
# VDD -> VREF 3.3V (Pin 17)
# AGND, DGND -> GND (Pin 25, 20)
# MOSI -> GPIO10 (Pin 19)
# MISO -> GPIO9 (Pin 21)
# CLK -> GPIO11 (Pin 23)


class ADC():
    def __init__(self):

        # Hardware SPI configuration:
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.mcp = MCP.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def read(self):

        values = []

        # Read values of 8 channels
        for pin in range(8):
            values[pin] = self.mcp.read_adc(pin)
        
        return values

adc = ADC()

if __name__ == "__main__":

    print("reading for 10 seconds")
    
    for reading in range(100):
        print(adc.read())
        time.sleep(0.1)