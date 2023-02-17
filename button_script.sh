#!/bin/bash

# set up the GPIO pin
echo 14 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio14/direction
echo high > /sys/class/gpio/gpio14/direction

# loop forever, waiting for the button press event
while true; do
    if [ "$(cat /sys/class/gpio/gpio14/value)" = "0" ]; then
        # call the main.py script when the button is pressed
        echo "Button pressed"
        python3 main.py
        # wait a short time to avoid multiple presses being detected
        sleep 0.5
    fi
done

# clean up the GPIO pin
echo 14 > /sys/class/gpio/unexport
