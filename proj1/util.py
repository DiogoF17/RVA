import math
import cv2 as cv
import numpy as np

# -----------------------------------------------------------------------

def orderCoordinates(quadrilateral):
    # Top Left (TL), Top Right(TR), Bottom Left(BL), Bottom Right(BR)
    # TL --- TR
    # |      |
    # |      |
    # BL --- BR
    coords = [coord for coord in quadrilateral.verticesCoords]
    
    sumCoords = [[coord[0] + coord[1], coord[1] - coord[0], coord] for coord in coords]
    sumCoords.sort(key = lambda x: (x[0], x[1]))
    
    topLeft = sumCoords[0][2]
    topRight = sumCoords[1][2]
    bottomLeft = sumCoords[2][2]
    bottomRight = sumCoords[3][2]

    # Horizontal Oriented
    if quadrilateral.width >= quadrilateral.height * 1.4:
        # print("HORIZONTAL")
        return [bottomLeft, topLeft, bottomRight, topRight]
    # Vertical Oriented
    elif quadrilateral.width <= quadrilateral.height * 0.6:
        # print("VERTICAL")
        return [topLeft, topRight, bottomLeft, bottomRight]
    # Diamond Oriented
    else:
        coords.sort(key = lambda x: (x[1], -x[0]))

        yDiffFurthest = abs(coords[-1][1] - coords[-3][1])
        xDiffClosest = abs(coords[-1][0] - coords[-2][0])

        # Extreme points are aligned (left most and right most point have the same y value)
        if coords[1][1] == coords[2][1]:
            
            # Tilted to the right
            if abs(coords[-1][0] - coords[-2][0]) < abs(coords[-1][0] - coords[-3][0]):
                # print("ALIGNED BUT TILTED TO THE RIGHT")
                return [coords[0], coords[1], coords[2], coords[3]]
            # Tilted to the left
            else:
                # print("ALIGNED BUT TILTED TO THE LEFT")
                return [coords[2], coords[0], coords[1], coords[3]]

        # card is extremely inclined, almost horizontal
        elif xDiffClosest > yDiffFurthest:

            # Tilted to the right
            if coords[1][0] < coords[2][0]:
                # print("EXTREMELY TILTED TO RIGHT")
                return [coords[0], coords[2], coords[1], coords[3]]
            # Tilted to the left
            else:
                # print("EXTREMELY TILTED TO LEFT")
                return [coords[2], coords[0], coords[3], coords[1]]

        # card is normally inclined, almost vertical
        else:
            # Tilted to the right
            if coords[1][0] > coords[2][0]:
                # print("NORMALLY TILTED TO RIGHT")
                return [coords[0], coords[1], coords[2], coords[3]]
            # Tilted to the left
            else:
                # print("NORMALLY TILTED TO LEFT")
                return [coords[1], coords[0], coords[3], coords[2]]

def getRankSuitImgFromCardImg(img):
    height, width, _ = img.shape
    
    numberOfPixelsHorizontal = math.floor(width * 0.2)
    numberOfPixelsVertical = math.floor(height * 0.3)

    rankSuitImg = img[:numberOfPixelsVertical, :numberOfPixelsHorizontal, :]

    return cv.resize(cv.resize(rankSuitImg, [33, 62]), (0,0), fx=4, fy=4)

def identifyRankAndSuit(img):
    grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binarizedImg = cv.threshold(grayImg, 127, 255, cv.THRESH_BINARY_INV)
    
    numLabels, labels, _, _ = cv.connectedComponentsWithStats(binarizedImg)

    kernel = np.ones((5,5),np.uint8)

    for i in range(1, numLabels):
        mask = (labels == i).astype("uint8") * 255
        # mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        cv.imshow(f"Mask {i}", mask)

        contours, _ = cv.findContours(image = mask, mode = cv.RETR_TREE, method = cv.CHAIN_APPROX_NONE)
        
        x, y, width, height = cv.boundingRect(contours[0])
        cv.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)