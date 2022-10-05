import cv2 as cv
import numpy as np
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage
import game.cards as cards
import random as rng
import math

# =============================GLOBAL VARIABLES================================

cardImages = {cards.ACE_SPADES: {"fileName": "./cards_simple/1Bs.png"},
              cards.ACE_HEARTS: {"fileName": "./cards_simple/1Bh.png"},
              cards.ACE_CLUBS: {"fileName": "./cards_simple/1Bc.png"},
              cards.ACE_DIAMONDS: {"fileName": "./cards_simple/1Bd.png"}}
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
            quadrilaterals.append(coordinates[:,0])
            copy = coordinates[:,0].copy()
            copy = np.concatenate(([copy[-1]],copy[:-1]))
            # lastElem = copy.pop(-1)
            # copy.insert(0, lastElem)
            quadrilaterals.append(copy)
    
    return quadrilaterals
    
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

def templateMatching(possibleCards, simple=True):
    for possibleCard in possibleCards:
        # if simple:
        #     numberOfPixelsHorizontal = math.floor(possibleCard.shape[1] * 0.25)
        #     numberOfPixelsVertical = math.floor(possibleCard.shape[0] * 0.3)
        #     cv.imshow("possibleCard2", possibleCard)
        #     possibleCard = cv.resize(possibleCard[:numberOfPixelsVertical, :numberOfPixelsHorizontal, :],[33,62])
        for card in cardImages:
            # Apply template Matching
            # possibleCard = cv.cvtColor(possibleCard, cv.COLOR_BGR2GRAY)
            # cardImages[card]["img"] = cv.cvtColor(cardImages[card]["img"], cv.COLOR_BGR2GRAY)
            # aux = cardImages[card]["img"][:numberOfPixelsVertical, :numberOfPixelsHorizontal, :]
            res = cv.matchTemplate(possibleCard,cardImages[card]["img"],cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            cv.imshow("possibleCard", possibleCard)
            if(max_val >= 0.6):
                # cv.imshow("possibleCard", possibleCard)
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
    
