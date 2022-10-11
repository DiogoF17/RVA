import cv2 as cv
import numpy as np
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage
import game.cards as cards
import game.templateCard as templateCard
from quadrilateral import Quadrilateral
from card import Card
import util
from connectedComponent import ConnectedComponent

# =============================GLOBAL VARIABLES================================

templateCards = []
templateCardsSimple = []

QUIT_KEY = ord("q")

MIN_AREA_OF_CARDS = 5000
MIN_MATCH_FOR_TEMPLATE = 0.7
MIN_MATCH_FOR_FEATURE = 20

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
        img = cv.resize(img, (0,0), fx=4, fy=4)
        # img = binarize(img)
        _, des = sift.detectAndCompute(img, None)
        templateCardsSimple.append(templateCard.TemplateCard(cards.templateCardsSimple[fileName], img, des))
    print("Set up Completed!")

# ---------------------------------------------------------------------

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
    
    return quadrilaterals
    
def detectPossibleCards(img):
    binarized = binarize(img)
    connectedComponents = detectConnectedComponents(binarized)
    quadrilaterals = detectQuadrilaterals(connectedComponents)
    
    return quadrilaterals

# ---------------------------------------------------------------------

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

def findBestTemplateMatch(possibleCard, simple = True):
    bestMatchValue = -1
    bestMatchName = None

    templateCardsToBeCompared = templateCards
    if simple:
        templateCardsToBeCompared = templateCardsSimple

    # possibleCard = binarize(possibleCard)
    cv.imshow(f"Image To Check", possibleCard)
    # cv.imshow(f"Template", binarize(templateCardsToBeCompared[0].img))

    # print("\n############################################\n")
    for method in [cv.TM_CCOEFF, cv.TM_CCOEFF_NORMED, cv.TM_CCORR,
        cv.TM_CCORR_NORMED, cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        for templateCardToBeCompared in templateCardsToBeCompared:

            res = cv.matchTemplate(possibleCard, templateCardToBeCompared.img, method)
            min_val, max_val, _, _ = cv.minMaxLoc(res)

            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                val = min_val
                if(val < bestMatchValue):
                    bestMatchValue = val
                    bestMatchName = templateCardToBeCompared.name
            else:
                val = max_val
                if(val > bestMatchValue):
                    bestMatchValue = val
                    bestMatchName = templateCardToBeCompared.name

        # print(f"Method: {method} | Val: {bestMatchValue} | Name: {bestMatchName}")

            # if(max_val >= MIN_MATCH_FOR_TEMPLATE and max_val > bestMatchValue):
            #     bestMatchValue = max_val
            #     bestMatchName = templateCardToBeCompared.name


        # diffImg = cv.absdiff(binarize(templateCardToBeCompared.img), possibleCard)
        # val = int(np.sum(diffImg)/255)

        # if(val > bestMatchValue):
        #     bestMatchValue = val
        #     bestMatchName = templateCardToBeCompared.name

    return bestMatchName, bestMatchValue

def templateMatching(possibleCard, simple = True):    
    imgToCheck = possibleCard.homography

    # get only the symbol of the card
    if simple:
        imgToCheck = util.getRankSuitImgFromCardImg(imgToCheck)
        util.identifyRankAndSuit(imgToCheck)
    
    matchName, matchValue = findBestTemplateMatch(imgToCheck, simple = simple)
    
    if(matchName != None):
        print(f"Card Name: {matchName} | Match Value: {matchValue}")
        return Card(possibleCard, matchName)

    return None

def featureMatching(possibleCard, simple = True):
    bestNumberOfMatches = -1
    bestMatchName = None

    imgToCheck = possibleCard.homography
    templateCardsToBeCompared = templateCards

    # get only the symbol of the card
    if simple:
        templateCardsToBeCompared = templateCardsSimple
        imgToCheck = util.getRankSuitImgFromCardImg(imgToCheck)
        util.identifyRankAndSuit(imgToCheck)
    
    cv.imshow(f"Image To Check", imgToCheck)

    sift = cv.SIFT_create()
    
    # imgToCheck = binarize(imgToCheck)
    _, des1 = sift.detectAndCompute(imgToCheck, None)
    
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
        return Card(possibleCard, bestMatchName)

    return None

def identifyPossibleCards(img, possibleCards, usingHomography = True, simple = True):
    identifiedCards = []
    index = 0
    if usingHomography:
        for possibleCard in possibleCards:
            possibleCard.homography = calculateHomographyAndWarpImage(img, possibleCard)
            
            # cv.imshow(f"Output {index}", possibleCard.homography)
            
            identifiedCard = templateMatching(possibleCard, simple = simple)
            # identifiedCard = featureMatching(possibleCard, simple = simple)
            if identifiedCard != None:
                identifiedCards.append(identifiedCard)

            index += 1
            
    return identifiedCards

# ---------------------------------------------------------------------

# 192.168.1.74:8080

def associatePlayersWithCards(detectedCards):
    # ---------------------------------
    # With 4 players
    #             Player 2 
    #  Player 1               Player 3
    #             Player 4
    # ---------------------------------
    # With 2 players
    #  Player 1              Player 2
    # ---------------------------------

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

# ---------------------------------------------------------------------

def showTextInImg(img, position, text):
    font = cv.FONT_HERSHEY_SIMPLEX  
    fontScale = 1
    color = (0, 255, 0)
    thickness = 2
    
    img = cv.putText(img, text, position, font, 
                    fontScale, color, thickness, cv.LINE_AA)

def announceRoundWinnerOrLoser(img, text, player, detectedCards):
    cardPosition = []
    
    for detectedCard in detectedCards:
        if detectedCard.player == player:
            cardPosition = detectedCard.quadrilateral.centroid

    if cardPosition == []:
        print("Could not show round winner")
        return  
    
    cardPosition[0] = max(0, cardPosition[0] - 5)
    showTextInImg(img, cardPosition, text)

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
    detectedCards = identifyPossibleCards(frame, detectedPossibleCards, simple = True)

    # Only continues processing if there is the right number of cards on the table
    if len(detectedCards) == cardsPerRound:
        # The person that played each card
        detectedCards = associatePlayersWithCards(detectedCards)

        game.gameRound(detectedCards)
        text, roundWinnerOrLoser = game.getRoundWinnerOrLoser()
        announceRoundWinnerOrLoser(frame, text, roundWinnerOrLoser, detectedCards)

        print("###############################")
    
    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break
    
cv.destroyAllWindows()
    