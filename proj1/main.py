import cv2 as cv
import numpy as np
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage
import game.cards as cards
import math
import game.templateCard as templateCard

# =============================GLOBAL VARIABLES================================

templateCards = []
templateCardsSimple = []

QUIT_KEY = ord("q")

MIN_AREA_OF_CARDS = 5000
MINIMUM_MATCH_FOR_TEMPLATE = 0.6

# ===============================FUNCTIONS=====================================

def setUp():
    # load normal template
    for fileName in cards.templateCards:
        img = cv.imread(fileName)
        templateCards.append(templateCard.TemplateCard(cards.templateCards[fileName], img))

    # load simple template
    for fileName in cards.templateCardsSimple:
        img = cv.imread(fileName)
        templateCardsSimple.append(templateCard.TemplateCard(cards.templateCardsSimple[fileName], img))

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

def detectQuadrilaterals(components, overlapping = False):
    quadrilaterals = []
    
    for component in components:
        contours, _ = cv.findContours(image=component, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
        coordinates = cv.approxPolyDP(contours[0], 0.04 * cv.arcLength(contours[0], True), True)

        # if overlapping is not allowed we only keep quadrilaterals
        if len(coordinates) != 4 and not overlapping:
            continue

        quadrilaterals.append(coordinates[:, 0])

        copy = coordinates[:, 0].copy()
        copy = np.concatenate(([copy[-1]], copy[:-1]))
        quadrilaterals.append(copy)
    
    return quadrilaterals
    
# return: quadrilaterals coordinates
def detectCards(img):
    binarized = binarize(img)
    connectedComponents = detectConnectedComponents(binarized)
    quadrilaterals = detectQuadrilaterals(connectedComponents)
    
    return quadrilaterals

def calculateHomographyAndWarpImage(img, coord_src, coord_dst = np.array([[0,0],[0,725],[499,725],[499,0]])):
    # coord_src and coord_dst are numpy arrays of points
    # in source and destination images. We need at least
    # corresponding points.
    homography, _ = cv.findHomography(coord_src, coord_dst)
    
    # The calculated homography can be used to warp
    # the source image to destination. Size is the
    # size (width,height) of result
    size = [coord_dst[2][0] + 1, coord_dst[2][1] + 1]
    result = cv.warpPerspective(img, homography, size)
    return result

def findBestTemplateMatch(card, simple = True):
    bestMatchValue = -1
    bestMatchName = ""

    templateCardsToBeCompared = templateCards
    if simple:
        templateCardsToBeCompared = templateCardsSimple

    for templateCard in templateCardsToBeCompared:
        res = cv.matchTemplate(card, templateCard.img, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)
        
        if(max_val >= MINIMUM_MATCH_FOR_TEMPLATE and max_val > bestMatchValue):
            bestMatchValue = max_val
            bestMatchName = templateCard.name

    return bestMatchName, bestMatchValue

def computeHomographies(img, cards):
    homographies = []

    for card in cards:
        homographies.append(calculateHomographyAndWarpImage(img, np.array(card)))

    return homographies

def templateMatching(img, cards, simple = True):
    homographies = computeHomographies(img, cards)

    for homography in homographies:
        
        # get only the symbol of the card
        if simple:
            numberOfPixelsHorizontal = math.floor(homography.shape[1] * 0.25)
            numberOfPixelsVertical = math.floor(homography.shape[0] * 0.3)
            homography = cv.resize(homography[:numberOfPixelsVertical, :numberOfPixelsHorizontal, :], [33, 62])
        
        matchName, matchValue = findBestTemplateMatch(homography, simple = simple)
        print(f"Card Name: {matchName} | Match Value: {matchValue}")

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

# return: {cardName: img}
def identifyCards(img, cards, usingTemplate = True, simple = True):
    if usingTemplate:
        templateMatching(img, cards, simple = simple)

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
def associatePlayersWithCards(cards):
    pass

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
    detectedCards = detectCards(frame)

    # Only continues processing if there is the right number of cards on the table
    if len(cards) == cardsPerRound:

        # Which card is which
        cardsNames = identifyCards(frame, cards)

        # The person that played each card
        playersAssociatedWithEachCard = associatePlayersWithCards(cardsNames)

        # game.gameRound(playersAssociatedWithEachCard)
        # roundWinner = game.getRoundWinner()
    
    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break
    
cv.destroyAllWindows()
    
