import cv2 as cv
import numpy as np
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage
import game.cards as cards
import math
import game.templateCard as templateCard
import time
from connectedComponent import ConnectedComponent
from quadrilateral import Quadrilateral
from card import Card
import util

# =============================GLOBAL VARIABLES================================

templateCards = []
templateCardsSimple = []

QUIT_KEY = ord("q")

MIN_AREA_OF_CARDS = 5000
MIN_MATCH_FOR_TEMPLATE = 0.7
MIN_MATCH_FOR_FEATURE = 40

# ===============================FUNCTIONS=====================================

def setUp():
    print("Setting up...")
    sift = cv.SIFT_create()
    # load normal template
    for fileName in cards.templateCards:
        img = cv.imread(fileName)
        _, des = sift.detectAndCompute(img, None)
        templateCards.append(templateCard.TemplateCard(cards.templateCards[fileName], img, des))

    # load simple template
    for fileName in cards.templateCardsSimple:
        img = cv.imread(fileName)
        templateCardsSimple.append(templateCard.TemplateCard(cards.templateCardsSimple[fileName], img, None))
    print("Set up Completed!")

def binarize(img, thresholdValue = 127):
    grayScaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binarized = cv.threshold(grayScaleImg, thresholdValue, 255, cv.THRESH_BINARY)
    return binarized

def detectConnectedComponents(img):
    numLabels, labels, stats, centroids = cv.connectedComponentsWithStats(img)
    
    connectedComponents = []
    for i in range(1, numLabels):            
        if stats[i, cv.CC_STAT_AREA] >= MIN_AREA_OF_CARDS:
            componentMask = (labels == i).astype("uint8") * 255
            connectedComponent = ConnectedComponent(componentMask, centroids[i])
            connectedComponents.append(connectedComponent)
    
    return connectedComponents

def detectQuadrilaterals(components, overlapping = False):
    quadrilaterals = []
    
    for component in components:
        contours, _ = cv.findContours(image=component.mask, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
        coordinates = cv.approxPolyDP(contours[0], 0.04 * cv.arcLength(contours[0], True), True)

        # if overlapping is not allowed we only keep quadrilaterals
        if len(coordinates) != 4 and not overlapping:
            continue

        quadrilateral = Quadrilateral(component.centroid, contours[0], coordinates[:, 0])
        quadrilaterals.append(quadrilateral)

        # copy = coordinates[:, 0].copy()
        # copy = np.concatenate(([copy[-1]], copy[:-1]))
        # quadrilaterals.append(copy)
    
    return quadrilaterals
    
def detectPossibleCards(img):
    binarized = binarize(img)
    connectedComponents = detectConnectedComponents(binarized)
    quadrilaterals = detectQuadrilaterals(connectedComponents)
    
    return quadrilaterals

def findBestTemplateMatch(possibleCard, simple = True):
    bestMatchValue = -1
    bestMatchName = None

    templateCardsToBeCompared = templateCards
    if simple:
        templateCardsToBeCompared = templateCardsSimple

    for templateCardToBeCompared in templateCardsToBeCompared:
        res = cv.matchTemplate(possibleCard, templateCardToBeCompared.img, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)
        
        if(max_val >= MIN_MATCH_FOR_TEMPLATE and max_val > bestMatchValue):
            bestMatchValue = max_val
            bestMatchName = templateCardToBeCompared.name

    return bestMatchName, bestMatchValue

def templateMatching(possibleCard, simple = True):    
    # get only the symbol of the card
    if simple:
        numberOfPixelsHorizontal = math.floor(possibleCard.homography.shape[1] * 0.25)
        numberOfPixelsVertical = math.floor(possibleCard.homography.shape[0] * 0.3)
        possibleCard.homography = cv.resize(possibleCard.homography[:numberOfPixelsVertical, :numberOfPixelsHorizontal, :], [33, 62])
    
    matchName, matchValue = findBestTemplateMatch(possibleCard.homography, simple = simple)
    
    if(matchName != None):
        print(f"Card Name: {matchName} | Match Value: {matchValue}")
        return Card(possibleCard, matchName)

    return None

def featureMatching(possibleCard):
    bestNumberOfMatches = -1
    bestMatchName = None
    
    sift = cv.SIFT_create()
    
    _, des1 = sift.detectAndCompute(possibleCard, None)
    
    templateCardsToBeCompared = templateCards
    
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
     
    flann = cv.FlannBasedMatcher(index_params, search_params)   
 
    for templateCardToBeCompared in templateCardsToBeCompared:
        
        matches = flann.knnMatch(des1, templateCardToBeCompared.descriptor, k=2)
        
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
                
        if (len(good) >= MIN_MATCH_FOR_FEATURE and len(good) > bestNumberOfMatches):
            bestNumberOfMatches = len(good)
            bestMatchName = templateCardToBeCompared.name
            
    if(bestMatchName != None):
        print(f"Card Name: {bestMatchName} | Nº Of Matches: {bestNumberOfMatches}")

def calculateHomographyAndWarpImage(img, quadrilateral, coord_dst = np.array([[0, 0], [499, 0], [0, 725], [499, 725]])):
    coord_src = np.array(util.orderCoordinates(quadrilateral))

    # coord_src and coord_dst are numpy arrays of points
    # in source and destination images. We need at least
    # corresponding points.
    homography, _ = cv.findHomography(coord_src, coord_dst)
    
    # The calculated homography can be used to warp
    # the source image to destination. Size is the
    # size (width,height) of result
    width = (coord_dst[1][0] - coord_dst[0][0]) + 1
    height = (coord_dst[2][1] - coord_dst[0][0]) + 1
    result = cv.warpPerspective(img, homography, [width, height])

    return result

def identifyPossibleCards(img, possibleCards, usingHomography = True, simple = True):
    identifiedCards = []
    index = 0
    if usingHomography:
        for possibleCard in possibleCards:
            possibleCard.homography = calculateHomographyAndWarpImage(img, possibleCard)
            
            cv.imshow(f"Output {index}", possibleCard.homography)
            
            identifiedCard = templateMatching(possibleCard, simple = simple)
            if identifiedCard != None:
                identifiedCards.append(identifiedCard)

            # featureMatching(homography)
            index += 1
            
    return identifiedCards

# 192.168.1.74:8080

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

def associatePlayersWithCards(detectedCards):
    xCentroid = []
    yCentroid = []
    
    for detectedCard in detectedCards:
        xCentroid.append([detectedCard.quadrilateral.centroid[0],detectedCard])
        yCentroid.append([detectedCard.quadrilateral.centroid[1],detectedCard])
        
    xCentroid.sort(key=(lambda x : x[0]))
    yCentroid.sort(key=(lambda x : x[0]))
        
    if len(detectedCards) == 2:
        xCentroid[0][1].player = 1
        xCentroid[3][1].player = 2
    else:
        xCentroid[0][1].player = 1
        xCentroid[3][1].player = 3
        
        yCentroid[0][1].player = 2
        yCentroid[3][1].player = 4
      
    return detectedCards

# ===================================MAIN======================================

setUp()

game = gamePackage.Game()
camera = remoteWebCamPackage.RemoteWebCam()

cardsPerRound = game.getCardsPerRound()

while True:
    camera.nextFrame()
    if not camera.validFrame():
        print("Couldn't get video from camera")
        print("Exiting...")
        break
    
    frame = camera.getFrame()
    
    # Where are the cards
    detectedPossibleCards = detectPossibleCards(frame)

    # Only continues processing if there is the right number of cards on the table
    # if len(detectedCards) == cardsPerRound:

    # Which card is which
    detectedCards = identifyPossibleCards(frame, detectedPossibleCards, simple=False)

    # Only continues processing if there is the right number of cards on the table
    if len(detectedCards) == cardsPerRound:
        # The person that played each card
        playersAssociatedWithEachCard = associatePlayersWithCards(frame, detectedCards)

        game.gameRound(playersAssociatedWithEachCard)
        roundWinner = game.getRoundWinner()

        print("###############################")
    
    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break

    # time.sleep(0.05)
    
cv.destroyAllWindows()
    