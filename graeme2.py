import picamera, time


with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    
    while(True):
        time.sleep(1)
        camera.capture('graeme_board.jpg')        
