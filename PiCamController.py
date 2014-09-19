# -*- coding: utf-8 -*-
import SimpleCV,time,picamera
from SimpleCV import Camera

import scipy.spatial.distance as spsd

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
        rawInput = raw_input()
        if(rawInput == "Y" or rawInput == "y"):
            return image
 
def getRectanglesFromImage(image):
    return[blob for blob in image.findBlobs(minsize = 50, maxsize = 40000) if blob.isRectangle(0.5)]

def getSpaces(image):
    BUFFER = 40

    
    rectangles = getRectanglesFromImage(image)
    #print spsd.pdist(rectangles)
    for rectangleOne in rectangles:
        image.show()
        

        drawingLayer = image.dl()
        rectangleOne.draw(layer=drawingLayer)

        image.show()
        time.sleep(0.5)
        rectangleOneLongestSide = max(rectangleOne.width(), rectangleOne.height())
        
        for rectangleTwo in rectangles:            
            if(rectangleOne != rectangleTwo):                
                rectangleTwoLongestSide = max(rectangleTwo.width(), rectangleTwo.height())
                distanceBetweenRectangles = spsd.pdist([(rectangleOne.centroid()[0], rectangleOne.centroid()[1]), (rectangleTwo.centroid()[0], rectangleTwo.centroid()[1])])
                if(distanceBetweenRectangles <= (rectangleOneLongestSide/2) + (rectangleTwoLongestSide/2) + BUFFER ):
                    rectangleTwo.draw(layer=drawingLayer, color=(0,0,128))                    
                    image.show()                    
                    print(rectangleOne, " ", rectangleTwo)
                    time.sleep(0.5)
        image.removeDrawingLayer()
    

#print "Welcome to GobletKingsGames, ",
#image = getAndVerifyImage()
image = getImage()

rectangles = getSpaces(image)
for rect in rectangles:
    time.sleep(2)
    rect.draw()
    image.show()

image.show()
time.sleep(25)
