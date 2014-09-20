# -*- coding: utf-8 -*-
import SimpleCV,time
from SimpleCV import Camera
from pygraph.classes.graph import graph
from pygraph.classes.exceptions import AdditionError
from xs_and_os_validator import validate_board

import scipy.spatial.distance as spsd
import math, freenect, cv


    

    

def getImage():
    video = freenect.sync_get_video()[0]
    video = video[:, :, ::-1]  # RGB -> BGR
    image = cv.CreateImageHeader((video.shape[1], video.shape[0]), cv.IPL_DEPTH_8U, 3)
    cv.SetData(image, video.tostring(),
               video.dtype.itemsize * 3 * video.shape[1])
    return (SimpleCV.ImageClass.Image(image) * 2).erode().erode()
    
##    (image, timestamp) = freenect.sync_get_video()
##    if(image is None):
##        print "What the fudge happened?"
##        exit()
##    else:
##        return SimpleCV.ImageClass.Image(image).erode().erode()
    

def getAndVerifyImage():
    while(True):
        image = getImage()    
        image.show()
        return image
 
def getRectanglesFromImage(image):
    blobs = image.findBlobs(minsize = 90, maxsize = 40000)
    if blobs is None:
        return None
    else:
        return[blob for blob in blobs if blob.isRectangle(0.5)]

def getNonRectangularBlobsFromImage(image):
    blobs = image.invert().findBlobs(minsize = 6, maxsize = 20000)
    if blobs is None:
        return None
    else:
        return blobs        


def getSpaces(image):      
    BUFFER = 90
    g = graph()

    
   
    pieces = getNonRectangularBlobsFromImage(image)
    rectangles = getRectanglesFromImage(image)
    if rectangles is None:
        return
    
    rectanglesToId = {}
    rectanglesToFill = {}
    nextId = 1

    #row, then y sorting
    newRectangles = []
    rectangles.sort(key=lambda rectum: rectum.x)
    rows = math.floor(math.sqrt(len(rectangles)))

    for (index, rectangle) in enumerate(rectangles):        
        row = math.floor(index/rows)        
        newRectangles.append((row, rectangle))
    newRectangles.sort(key=lambda rectum: (rectum[0], rectum[1].y))

    #get average
    averageLength = sum([max(rectum.width(), rectum.height()) for rectum in rectangles])/len(rectangles)    
    BUFFER = averageLength/2
    
    
    for (row, r) in newRectangles:
        #find overlapping
        drawingLayer = image.dl()
        r.draw(layer=drawingLayer)

        overlapping = False

        if pieces is not None:
            for piece in pieces:            
                if(r.overlaps(piece)):
                    overlapping = True
                    piece.draw(layer=drawingLayer, color=(120,120,0))
                    break
                


        image.show()
	#time.sleep(1)
        image.removeDrawingLayer(-1)
        #find overlapping end        
        
        rectanglesToId[r] = str(nextId)
        rectanglesToFill[r] = overlapping
        g.add_node(str(nextId))
        nextId += 1
    for (row, rectangleOne) in newRectangles:       
        drawingLayer = image.dl()
        rectangleOne.draw(layer=drawingLayer)
        image.show()
        #time.sleep(0.1)
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

        image.show() 
	#time.sleep(0.1)
        image.removeDrawingLayer(-1)
    return (g, rectanglesToFill)

def getGraph():
    while(True):        
        spaces = getSpaces(getAndVerifyImage())
        #spaces = getSpaces(getImage())
        if spaces is not None and validate_board(spaces[0]):
            print "You've made a valid board"
            for space in spaces[1]:                
                print(space, spaces[1][space]) 
            return spaces
        else:
            print "Your board is invalid - try again!"
        

getGraph()

