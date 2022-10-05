import cv2 as cv
import numpy as np
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage
import game.cards as cards
import random as rng
import math

# =============================GLOBAL VARIABLES================================

cardImages = {cards.ACE_SPADES: {"fileName": "./cards_normal/1B.png"},
              cards.ACE_HEARTS: {"fileName": "./cards_normal/2B.png"},
              cards.ACE_CLUBS: {"fileName": "./cards_normal/3B.png"},
              cards.ACE_DIAMONDS: {"fileName": "./cards_normal/4B.png"}}
QUIT_KEY = ord("q")
MIN_AREA_OF_CARDS = 5000

# ===============================FUNCTIONS=====================================

def setUp():
    for card in cardImages:
        img = cv.imread(cardImages[card]["fileName"])
        cardImages[card]["img"] = img

def binarize(img, thresholdValue = 127):
    grayScaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binarized = cv.threshold(grayScaleImg, thresholdValue, 255, cv.THRESH_BINARY)
    return binarized

def detectConnectedComponents(img):
    numLabels, labels, stats, _ = cv.connectedComponentsWithStats(img)
    
    connectedComponents = []
    for i in range(1, numLabels):            
        if stats[i, cv.CC_STAT_AREA] >= MIN_AREA_OF_CARDS:
            componentMask = (labels == i).astype("uint8") * 255
            connectedComponents.append(componentMask)
    
    return connectedComponents

def detectQuadrilaterals(img, components):
    quadrilaterals = []
    
    for component in components:
        contours, _ = cv.findContours(image=component, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
        coordinates = cv.approxPolyDP(contours[0], 0.04 * cv.arcLength(contours[0], True), True)

        if len(coordinates) == 4:
            # color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            # cv.drawContours(img, contours, 0, color, 2, cv.LINE_8)
            # for coord in coordinates:
            #     cv.circle(img, (coord[0][0],coord[0][1]), radius=10, color=color, thickness=-1)
            quadrilaterals.append(formatCoordinates(coordinates))
    
    return quadrilaterals

# remove unecessary dimension
# [[[32,34]],[[23,67]]] to [[32,34],[23,67]]          
def formatCoordinates(coordinates):
    #      *
    #  *
    #         *
    #     *
    newCoordinates = []

    # ind = 0
    for i in range(4):
        # print(ind)
        # newCoordinates.append(coordinates[ind][0])

        # nextPoint1 = (i + 1) % 4
        # nextPoint2 = (i + 2) % 4
        # nextPoint3 = (i + 3) % 4

        # distPoint1 = math.sqrt(math.pow(coordinates[ind][0][0] - coordinates[nextPoint1][0][0], 2) +  math.pow(coordinates[ind][0][1] - coordinates[nextPoint1][0][1], 2))
        # distPoint2 = math.sqrt(math.pow(coordinates[ind][0][0] - coordinates[nextPoint2][0][0], 2) +  math.pow(coordinates[ind][0][1] - coordinates[nextPoint2][0][1], 2))
        # distPoint3 = math.sqrt(math.pow(coordinates[ind][0][0] - coordinates[nextPoint3][0][0], 2) +  math.pow(coordinates[ind][0][1] - coordinates[nextPoint3][0][1], 2))
        
        # dists = [[distPoint1, nextPoint1], [distPoint2, nextPoint2], [distPoint3, nextPoint3]]
        # dists.sort(key = lambda x: x[0])
        # print(dists)
        # if i % 2 == 0: # menor distancia
        #     ind = dists[0][1]
        # else:
        #     ind = dists[1][1]
        newCoordinates.append(coordinates[i][0])
        

    # print(ind)
    # newCoordinates.append(coordinates[ind][0])
    # print(newCoordinates)
    return newCoordinates
    
# return: img with only the cards
def detectCards(img):
    binarized = binarize(img)
    connectedComponents = detectConnectedComponents(binarized)
    quadrilaterals = detectQuadrilaterals(img, connectedComponents)
    return img, quadrilaterals


# return: {cardName: img}
def identifyCards(img, possibleCardsPosition):
    possibleCards = []
    for coordinates in possibleCardsPosition:
        possibleCards.append(calculateHomographyAndWarpImage(img, np.array(coordinates)))
    templateMatching(possibleCards)
   
def calculateHomographyAndWarpImage(img, coord_src, coord_dst = np.array([[0,0],[0,725],[499,725],[499,0]])):
    # coord_src and coord_dst are numpy arrays of points
    # in source and destination images. We need at least
    # corresponding points.
    h, status = cv.findHomography(coord_src, coord_dst)
    
    # The calculated homography can be used to warp
    # the source image to destination. Size is the
    # size (width,height) of result
    size = [coord_dst[2][0]+1,coord_dst[2][1]+1]
    result = cv.warpPerspective(img, h, size)
    return result

def templateMatching(possibleCards):
    for possibleCard in possibleCards:
        for card in cardImages:
            # Apply template Matching
            res = cv.matchTemplate(possibleCard,cardImages[card]["img"],cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if(max_val >= 0.70):
                cv.imshow("possibleCard", possibleCard)
                print("Card name: "+card + f" max_val={max_val}")


# 192.168.1.74:8080

# def featureMatching(round):
#     detectedCard = None
#     numberOfMatches = -1
    
#     sift = cv.SIFT_create()
    
#     _, des1 = sift.detectAndCompute(round, None)
#     for card in cardImages:
#         _, des2 = sift.detectAndCompute(cardImages[card]["img"], None)
        
#         FLANN_INDEX_KDTREE = 1
#         index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#         search_params = dict(checks = 50)
        
#         flann = cv.FlannBasedMatcher(index_params, search_params)
#         matches = flann.knnMatch(des1, des2, k=2)
        
#         # store all the good matches as per Lowe's ratio test.
#         good = []
#         for m,n in matches:
#             if m.distance < 0.7 * n.distance:
#                 good.append(m)
                
#         if len(good) > numberOfMatches:
#             detectedCard = card
#             numberOfMatches = len(good)
        
#     print(f"Detected: {detectedCard}")
    

# return: {cardName: playerName}
# ---------------------------------
# With 4 players
#             Player 2 
#  Player 1               Player 3
#             Player 4
# ---------------------------------
# With 2 players
#  Player 1              Player 2
# ---------------------------------
def associatePlayersWithCards(cards):
    pass

# ===================================MAIN======================================

setUp()

game = gamePackage.Game()
camera = remoteWebCamPackage.RemoteWebCam()

while True:
    camera.nextFrame()
    if not camera.validFrame():
        print("Couldn't get video from camera")
        print("Exiting...")
        break
    
    frame = camera.getFrame()
    
    # Where are the cards
    frame, possibleCardsPosition = detectCards(frame)
    
    if(len(possibleCardsPosition) != 0 ):
        # Which card is which
        cardsNames = identifyCards(frame, possibleCardsPosition)
    # # The person that played each card
    # playersAssociatedWithEachCard = associatePlayersWithCards(cardsNames)

    # game.gameRound(playersAssociatedWithEachCard)
    # roundWinner = game.getRoundWinner()
    
    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break
    
cv.destroyAllWindows()
    
