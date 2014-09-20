import SimpleCV,time,picamera
from SimpleCV import Camera


def takePicture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.brightness = 70
        camera.contrast = 100
        camera.saturation = 100
        camera.start_preview()
        
        time.sleep(5)
        camera.capture('board.jpg')

def getImage():
    image = SimpleCV.Image("board.jpg")
    if(image is None):
        print "What the fudge happened?"
        exit()
    else:
        return image.erode().erode()
    

def getAndVerifyImage():
    while(True):
        print("Press Enter to take photo of your board, you will have a 5 second preview")
        raw_input()
        takePicture()
        image = getImage()    
        image.show()
        print("Is this your image(Y/N)?")

        if(raw_input() == "Y" or raw_input() == "y"):
                return image
def getRectanglesFromImage(image):
    blobs = image.findBlobs(minsize = 200)
    return [blob for blob in blobs if blob.isRectangle(0.5)]

print "Welcome to GobletKingsGames, ",
image = getAndVerifyImage()
print "graeme"
getRectanglesFromImage(image)
