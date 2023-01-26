import time
import Adafruit_MCP3008 as MCP

# Pin config:

# CS GPIO8 (Pin 24)
# VDD, VREF 3.3V (Pin 17)
# AGND, DGND GND (Pin 25, 20)
# MOSI GPIO10 (Pin 19)
# MISO GPIO9 (Pin 21)
# CLK GPIO11 (Pin 23)
# GND (Pin 25)

class ADC():
    def __init__(self):

        # Hardware SPI configuration:
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0
        self.mcp = MCP.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def read(self):

        # Initialize array with 8 zeroes
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