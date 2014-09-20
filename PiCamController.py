# -*- coding: utf-8 -*-
import SimpleCV,time,picamera
from SimpleCV import Camera
from pygraph.classes.graph import graph
from pygraph.classes.exceptions import AdditionError
from xs_and_os_validator import validate_board

import scipy.spatial.distance as spsd
import math

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

def getNonRectangularBlobsFromImage(image):
    return[blob for blob in image.invert().findBlobs(minsize = 10, maxsize = 20000)]

def getSpaces(image):      
    BUFFER = 90
    g = graph()

    
   
    pieces = getNonRectangularBlobsFromImage(image)
    rectangles = getRectanglesFromImage(image)
    rectanglesToId = {}
    rectanglesToFill = {}
    nextId = 1

    #row, then y sorting
    newRectangles = []
    rectangles.sort(key=lambda rectum: rectum.x)
    rows = math.floor(math.sqrt(len(rectangles)))
    print(rows)
    for (index, rectangle) in enumerate(rectangles):        
        row = math.floor(index/rows)        
        newRectangles.append((row, rectangle))
    newRectangles.sort(key=lambda rectum: (rectum[0], rectum[1].y))
    
    for (row, r) in newRectangles:
        #find overlapping
        drawingLayer = image.dl()
        r.draw(layer=drawingLayer)

        overlapping = False
        
        for piece in pieces:            
            if(r.overlaps(piece)):
                overlapping = True        
                piece.draw(layer=drawingLayer, color=(120,120,0))

        image.show()
        image.removeDrawingLayer()
        #find overlapping end
        
        rectanglesToId[r] = str(nextId)
        rectanglesToFill[r] = overlapping
        g.add_node(str(nextId))
        nextId += 1
    for (row, rectangleOne) in newRectangles:       
        #drawingLayer = image.dl()
        #rectangleOne.draw(layer=drawingLayer)
        #image.show()
        #time.sleep(0.25)
        rectangleOneLongestSide = max(rectangleOne.width(), rectangleOne.height())
        
        for (row, rectangleTwo) in newRectangles:            
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

        #image.show() 
        #image.removeDrawingLayer()
    return (g, rectanglesToFill)

def getGraph():
    while(True):        
        spaces = getSpaces(getImage())
        if validate_board(spaces[0]):
            print "You've made a valid board"
            for space in spaces[1]:                
                print(space, spaces[1][space])
            time.sleep(200)
            return spaces
        else:
            print "Your board is invalid - try again!"
        

getGraph()

