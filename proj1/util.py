import math
import cv2 as cv

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
        print("HORIZONTAL")
        return [bottomLeft, topLeft, bottomRight, topRight]
    # Vertical Oriented
    elif quadrilateral.width <= quadrilateral.height * 0.6:
        print("VERTICAL")
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
                print("ALIGNED BUT TILTED TO THE RIGHT")
                return [coords[0], coords[1], coords[2], coords[3]]
            # Tilted to the left
            else:
                print("ALIGNED BUT TILTED TO THE LEFT")
                return [coords[2], coords[0], coords[1], coords[3]]

        # card is extremely inclined, almost horizontal
        elif xDiffClosest > yDiffFurthest:

            # Tilted to the right
            if coords[1][0] < coords[2][0]:
                print("EXTREMELY TILTED TO RIGHT")
                return [coords[0], coords[2], coords[1], coords[3]]
            # Tilted to the left
            else:
                print("EXTREMELY TILTED TO LEFT")
                return [coords[2], coords[0], coords[3], coords[1]]

        # card is normally inclined, almost vertical
        else:
            # Tilted to the right
            if coords[1][0] > coords[2][0]:
                print("NORMALLY TILTED TO RIGHT")
                return [coords[0], coords[1], coords[2], coords[3]]
            # Tilted to the left
            else:
                print("NORMALLY TILTED TO LEFT")
                return [coords[1], coords[0], coords[3], coords[2]]

def getSuitImgFromCardImg(img):
    height, width, _ = img.shape
    
    numberOfPixelsHorizontal = math.floor(width * 0.2)
    numberOfPixelsVertical = math.floor(height * 0.3)

    return cv.resize(img[:numberOfPixelsVertical, :numberOfPixelsHorizontal, :], [33, 62])