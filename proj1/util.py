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
    
    numberOfPixelsHorizontal = math.floor(width * 0.17)
    numberOfPixelsVertical = math.floor(height * 0.3)

    rankSuitImg = img[:numberOfPixelsVertical, 10:80, :]

    return cv.resize(cv.resize(rankSuitImg, [33, 62]), (0,0), fx=4, fy=4)

def identifyRankAndSuit(img):
    # binarize img
    grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binarizedImg = cv.threshold(grayImg, 180, 255, cv.THRESH_BINARY_INV)
    
    cv.imshow("bin", binarizedImg)
    
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
        
        # temp = abs(1 - width/height)
        # if temp <= 0.3:
        boundingRects.append([x, y, width, height])
            # print(f"Width {width} | Height {height} | Temp {temp}")
        # else:
            # cv.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 2)
            # print(f"Width2 {width} | Height2 {height} | Temp {temp}")

    # it has to be exatly a rank and a suit
    # len(boundingRects) == 3 in case of rank 10
    if len(boundingRects) != 2 and len(boundingRects) != 3:
        return None

    # sort by y value
    # y value of rank is less than suit
    boundingRects.sort(key = lambda x: (x[1], x[0]))

    # dimensions of image
    height, width, _ = img.shape

    # padding = 10
    
    # card rank 10
    if len(boundingRects) == 3:
        # img of rank
        rankX, rankY, rankWidth, rankHeight = boundingRects[0]
        rankXB, _,    rankWidthB, rankHeightB = boundingRects[1]
        
        # added padding and assured that it not exceeded image dimensions
        # rankX1 = max(0, rankX - padding)
        # rankY1 = max(0, rankY - padding)
        # rankX2 = min(width - 1, rankX + rankWidth + padding)
        # rankY2 = min(height - 1, rankY + rankHeight + padding)
        # rankImg = img[rankY1 : rankY2, rankX1 : rankX2, :]
        rankImg = binarizedImg[rankY : rankY+rankHeight, rankX : rankXB + rankWidthB]

        suitX, suitY, suitWidth, suitHeight = boundingRects[2]
    else:
        # img of rank
        rankX, rankY, rankWidth, rankHeight = boundingRects[0]
        # added padding and assured that it not exceeded image dimensions
        # rankX1 = max(0, rankX - padding)
        # rankY1 = max(0, rankY - padding)
        # rankX2 = min(width - 1, rankX + rankWidth + padding)
        # rankY2 = min(height - 1, rankY + rankHeight + padding)
        # rankImg = img[rankY1 : rankY2, rankX1 : rankX2, :]
        rankImg = binarizedImg[rankY : rankY+rankHeight, rankX : rankX + rankWidth]

        suitX, suitY, suitWidth, suitHeight = boundingRects[1]
        
    rankImg = cv.resize(rankImg, [33, 62])
    
    # img of suit
    # suitX, suitY, suitWidth, suitHeight = boundingRects[1]
    # added padding and assured that it not exceeded image dimensions
    # suitX1 = max(0, suitX - padding)
    # suitY1 = max(0, suitY - padding)
    # suitX2 = min(width - 1, suitX + suitWidth + padding)
    # suitY2 = min(height - 1, suitY + suitHeight + padding)
    # suitImg = img[suitY1 : suitY2, suitX1 : suitX2, :]
    suitImg = binarizedImg[suitY : suitY+suitHeight, suitX : suitX + suitWidth]
    suitImg = cv.resize(suitImg, [33, 62])
    
    cv.imshow("Rank", rankImg)
    cv.imshow("Suit", suitImg)
    
    # draw bounding rect in rank suit img
    # for (x, y, width, height) in boundingRects:
    #     cv.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)

    return rankImg, suitImg


