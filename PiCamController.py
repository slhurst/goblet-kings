# -*- coding: utf-8 -*-
import SimpleCV,time,picamera
from SimpleCV import Camera
from pygraph.classes.graph import graph
from pygraph.classes.exceptions import AdditionError
from square_grid_validator import validate_board

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
        return image #.erode().erode()
    

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
    BUFFER = 90
    g = graph()
    
    rectangles = getRectanglesFromImage(image)
    rectanglesToId = {}
    nextId = 1
    for r in rectangles:
        rectanglesToId[r] = str(nextId)
        g.add_node(str(nextId))
        nextId += 1
    #print spsd.pdist(rectangles)
    for rectangleOne in rectangles:
##        image.show()
        

        drawingLayer = image.dl()
        rectangleOne.draw(layer=drawingLayer)

        image.show()
        time.sleep(0.25)
        rectangleOneLongestSide = max(rectangleOne.width(), rectangleOne.height())
        
        for rectangleTwo in rectangles:            
            if(rectangleOne != rectangleTwo):                
                rectangleTwoLongestSide = max(rectangleTwo.width(), rectangleTwo.height())
                distanceBetweenRectangles = spsd.pdist([(rectangleOne.centroid()[0], rectangleOne.centroid()[1]), (rectangleTwo.centroid()[0], rectangleTwo.centroid()[1])])
                if(distanceBetweenRectangles <= (rectangleOneLongestSide/2) + (rectangleTwoLongestSide/2) + BUFFER ):
                    try:
                        g.add_edge((rectanglesToId[rectangleOne], rectanglesToId[rectangleTwo]))
                    except AdditionError:
                        pass
                    rectangleTwo.draw(layer=drawingLayer, color=(0,0,128))                    
                                       
                    print(rectangleOne, " ", rectangleTwo)
##                    time.sleep(0.25)
        image.show() 
        image.removeDrawingLayer()
    return g

print "Welcome to GobletKingsGames, ",
image = getAndVerifyImage()
image = getImage()

g = getSpaces(image)
if validate_board(g):
    print "You've made a valid board"
else:
    print "Your board is invalid - try again!"

