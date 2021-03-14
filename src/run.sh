#!/bin/bash

sleep 5s
/usr/bin/python3  /home/pi/rpi-weatherboard/src/run.py >  /home/pi/rpi-weatherboard/log.log 2>&1
