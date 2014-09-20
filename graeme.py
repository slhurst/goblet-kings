import SimpleCV,time
from SimpleCV import Camera



#while(True):
image = SimpleCV.Image("/home/pi/scritps/board.jpg")


image.show()
time.sleep(0.25)
image = image.erode()
image.show()
blobs = image.findBlobs(minsize = 100)
for blob in blobs:
    if blob.isRectangle(0.5):
        time.sleep(0.25)
        print("Rectangle")
        blob.draw()

        image.show()

time.sleep(25)
