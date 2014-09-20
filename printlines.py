import SimpleCV

def drawLinesOnimage(image, lines):
    for line in lines:
        image.drawLine(line.points[0], line.points[1], (0, 0,255), 3)
