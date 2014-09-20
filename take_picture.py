#!/usr/bin/env python

import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.brightness = 70
    camera.contrast = 100
    camera.saturation = 100
    camera.start_preview()
    # Camera warm-up time
    time.sleep(5)
    camera.capture('board.jpg')
