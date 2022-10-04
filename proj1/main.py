import cv2 as cv
import numpy as np
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage
import game.cards as cards

templateCards = {cards.ACE_SPADES: {"fileName": "./cards_normal/1.png"},
              cards.ACE_HEARTS: {"fileName": "./cards_normal/2.png"},
              cards.ACE_CLUBS: {"fileName": "./cards_normal/3.png"},
              cards.ACE_DIAMONDS: {"fileName": "./cards_normal/4.png"}}

MIN_AREA_OF_CARDS = 5000

def setUp(featureTracking = True):
    sift = cv.SIFT_create()
    
    for card in templateCards:
        img = cv.imread(templateCards[card]["fileName"])
        templateCards[card]["img"] = img
        
        if featureTracking:
            _, descriptor = sift.detectAndCompute(img, None)
            templateCards[card]["descriptor"] = descriptor

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
            # componentMask = fillComponent(componentMask, 255)
            connectedComponents.append(componentMask)
    
    return connectedComponents

# fill the holes of each component
def fillComponent(component, fillColor):
    for i in range(len(component)):
        # find first index different from 0
        firstIndex = -1
        for j in range(len(component[i])):
            if component[i][j] != 0:
                firstIndex = j
                
        # find last index different from 0
        lastIndex = -1
        for j in range(len(component[i]) - 1, -1, -1):
            if component[i][j] != 0:
                lastIndex = j
                
        component[i][firstIndex : lastIndex + 1] = fillColor
        
    return component

def detectQuadrilaterals(components, overlapping = False):    
    quadrilaterals = []
    
    for component in components:
        contours, _ = cv.findContours(image=component, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
        numberOfSides = cv.approxPolyDP(contours[0], 0.04 * cv.arcLength(contours[0], True), True)
    
        # if overlapping is not allowed we only keep quadrilaterals
        if len(numberOfSides) != 4 and not overlapping:
            continue

        quadrilaterals.append(component)
            
    return quadrilaterals

def detectCardsFromQuadrilaterals(quadrilaterals, img):
    cards = []
    
    for quadrilateral in quadrilaterals:
        cards.append(cv.bitwise_and(img, img, mask = quadrilateral))

    return cards

# creates a mask with the several detected components
def getMask(imgShape, components):
    mask = np.zeros(imgShape, dtype="uint8")

    for component in components:
        mask = cv.bitwise_or(mask, component)

    return mask

def segmentImg(quadrilaterals, img):
    mask = getMask((img.shape[0], img.shape[1]), quadrilaterals)
    cards = cv.bitwise_and(img, img, mask = mask)
    return cards

# return: img with only the cards
def detectCardsAndSegmentImg(img):
    binarized = binarize(img, 100)
    connectedComponents = detectConnectedComponents(binarized)
    quadrilaterals = detectQuadrilaterals(connectedComponents)
    cards = detectCardsFromQuadrilaterals(quadrilaterals, img)
    
    segementedImg = segmentImg(quadrilaterals, img)
    
    return (cards, segementedImg)

# using FEATURE MATCHING
# return: {cardName: img}
def identifyCards(detectedCards):
    sift = cv.SIFT_create()
    
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
            
    flann = cv.FlannBasedMatcher(index_params, search_params)
    
    for detectedCard in detectedCards:
        bestCard = None
        numberOfMatches = -1
        
        _, detectedCardDescriptor = sift.detectAndCompute(detectedCard, None)
        for templateCard in templateCards:
            templateCardDescriptor = templateCards[templateCard]["descriptor"]
            matches = flann.knnMatch(detectedCardDescriptor, templateCardDescriptor, k=2)
            
            # store all the good matches as per Lowe's ratio test.
            good = []
            for m,n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)
            
            # verifies if there was more good matches with this template card
            # than the other, if so we think that the template card is the detected one
            if len(good) > numberOfMatches:
                bestCard = templateCard
                numberOfMatches = len(good)
        
        print(f"Detected: {bestCard}")

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

# ==================================================================

setUp()

QUIT_KEY = ord("q")

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
    cards, segmentedImg = detectCardsAndSegmentImg(frame)

    # Only continues processing if there is the right number of cards on the table
    if len(cards) == cardsPerRound:

        # Which card is which
        cardsNames = identifyCards(cards)

        # The person that played each card
        playersAssociatedWithEachCard = associatePlayersWithCards(cardsNames)

        # game.gameRound(playersAssociatedWithEachCard)
        # roundWinner = game.getRoundWinner()
    
    cv.imshow("video", segmentedImg)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break
    
cv.destroyAllWindows()
    
