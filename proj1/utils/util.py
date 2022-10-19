import math
import cv2 as cv

# -----------------------------------------------------------------------

MIN_AREA_FOR_RANK_AND_SUIT = 1000

# -----------------------------------------------------------------------

def orderCoordinates(quadrilateral):
    # Top Left (TL), Top Right(TR), Bottom Left(BL), Bottom Right(BR)
    # TL --- TR
    # |      |
    # |      |
    # BL --- BR
    coords = [coord for coord in quadrilateral.verticesCoords]
    
    sumCoords = [[coord[0] + coord[1], - coord[1], coord] for coord in coords]
    sumCoords.sort(key = lambda x: (x[0], x[1]))
    
    topLeft = sumCoords[0][2]
    topRight = sumCoords[1][2]
    bottomLeft = sumCoords[2][2]
    bottomRight = sumCoords[3][2]

    # Horizontal Oriented
    if quadrilateral.width >= quadrilateral.height * 1.4:
        if sumCoords[2][1] > sumCoords[1][1]:
            return [bottomLeft, bottomRight, topLeft, topRight]
        
        return [bottomLeft, topLeft, bottomRight, topRight]
    # Vertical Oriented
    elif quadrilateral.width <= quadrilateral.height * 0.6:
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
                return [coords[0], coords[1], coords[2], coords[3]]
            # Tilted to the left
            else:
                return [coords[2], coords[0], coords[1], coords[3]]

        # card is extremely inclined, almost horizontal
        elif xDiffClosest > yDiffFurthest:

            # Tilted to the right
            if coords[1][0] < coords[2][0]:
                return [coords[0], coords[2], coords[1], coords[3]]
            # Tilted to the left
            else:
                return [coords[2], coords[0], coords[3], coords[1]]

        # card is normally inclined, almost vertical
        else:
            # Tilted to the right
            if coords[1][0] > coords[2][0]:
                return [coords[0], coords[1], coords[2], coords[3]]
            # Tilted to the left
            else:
                return [coords[1], coords[0], coords[3], coords[2]]

def getRankSuitImgFromCardImg(img):
    height, _, _ = img.shape
    
    numberOfPixelsHorizontal = 80
    numberOfPixelsVertical = math.floor(height * 0.3)

    rankSuitImg = img[:numberOfPixelsVertical, 10:numberOfPixelsHorizontal, :]

    return cv.resize(cv.resize(rankSuitImg, [33, 62]), (0,0), fx=4, fy=4)

def identifyRankAndSuit(img):
    # binarize img
    grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binarizedImg = cv.threshold(grayImg, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    
    # detect connected components
    numLabels, labels, stats, _ = cv.connectedComponentsWithStats(binarizedImg)
    
    # both the rank and suit have to have a considerable area, in comparison to noise
    masks = []
    for i in range(1, numLabels):
        if stats[i, cv.CC_STAT_AREA] >= MIN_AREA_FOR_RANK_AND_SUIT:
            masks.append((labels == i).astype("uint8") * 255)

    # identify bounding rectangle of both rank and suit
    boundingRects = []
    for mask in masks:
        contours, _ = cv.findContours(image = mask, mode = cv.RETR_TREE, method = cv.CHAIN_APPROX_NONE)
        x, y, width, height = cv.boundingRect(contours[0])        
        boundingRects.append([x, y, width, height])

    # it has to be exatly a rank or 2 in case of 10 and a suit
    if len(boundingRects) != 2 and len(boundingRects) != 3:
        return None

    # sort by y value and x value
    # y value of rank is less than suit
    # on rank 10 the x of 1 is smaller than of 0
    boundingRects.sort(key = lambda x: (x[1], x[0]))
    
    # card rank 10
    if len(boundingRects) == 3:
        rankX, rankY, rankWidth, rankHeight = boundingRects[0]
        rankXB, rankYB, rankWidthB, rankHeightB = boundingRects[1]
        
        if rankXB > rankX:
            rankWidth = (rankXB + rankWidthB) - rankX
        else:
            rankWidth = (rankX + rankWidth) - rankXB
            rankX = rankXB
        
        if rankYB < rankY:
            rankY = rankYB
        
        if rankHeight < rankHeightB:
            rankHeight = rankHeightB
        
        suitX, suitY, suitWidth, suitHeight = boundingRects[2]
    else:
        rankX, rankY, rankWidth, rankHeight = boundingRects[0]
        suitX, suitY, suitWidth, suitHeight = boundingRects[1]
        
    # img of rank
    rankImg = binarizedImg[rankY : rankY + rankHeight, rankX : rankX + rankWidth]
    rankImg = cv.resize(rankImg, [33, 62])
    
    # img of suit
    suitImg = binarizedImg[suitY : suitY + suitHeight, suitX : suitX + suitWidth]
    suitImg = cv.resize(suitImg, [33, 62])
    
    return rankImg, suitImg
