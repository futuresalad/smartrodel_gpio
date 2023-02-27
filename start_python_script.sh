#!/bin/bash

while true; do
    if [ "$(cat /sys/class/gpio/gpio26/value)" = "0" ]; then
        
        echo "Button pressed"
        python3 main.py

        # Multipress prevention
        sleep 0.5

        echo "Recording finished, copying files"
        cp -r -n "./messdaten" "/media/usb"
        echo "All files copied"
    fi

done