#!/bin/bash

sleep 1

# clean up the GPIO pin
echo 26 > /sys/class/gpio/unexport

# set up the GPIO pin
echo 26 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio26/direction
echo high > /sys/class/gpio/gpio26/direction

cd smartrodel_gpio
echo "Button listener started"

while true; do
    if [ "$(cat /sys/class/gpio/gpio26/value)" = "0" ]; then
        
        echo "Button pressed"
        runuser -l pi -c 'python3 ~/smartrodel_gpio/main.py'

        # Multipress prevention
        sleep 0.5

        echo "Recording finished"
    fi

done

# clean up the GPIO pin
echo 26 > /sys/class/gpio/unexport
