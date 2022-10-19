import cv2 as cv
import numpy as np
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage
import game.cards as cards
import game.templateCard as templateCard
from utils.quadrilateral import Quadrilateral
from game.card import Card
import utils.util as util
from utils.connectedComponent import ConnectedComponent
from augmentedReality import showTrophy

# =============================GLOBAL VARIABLES================================

templateCardsRanks = []
templateCardsSuits = []

QUIT_KEY = ord("q")

MIN_AREA_OF_CARDS = 5000
MIN_MATCH_FOR_TEMPLATE = 0.8

# ===============================FUNCTIONS=====================================

def setUp():
    print("Setting up...")
    
    # load ranks template
    for fileName in cards.templateCardsRanks:
        img = cv.imread(fileName,0)
        templateCardsRanks.append(templateCard.TemplateCard(cards.templateCardsRanks[fileName], img, None))
        
    # load suit template
    for fileName in cards.templateCardsSuits:
        img = cv.imread(fileName,0)
        templateCardsSuits.append(templateCard.TemplateCard(cards.templateCardsSuits[fileName], img, None))
    
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
        
        # refine quadrilateral coords
        # define the criteria to stop. We stop it after a specified number of iterations
        # or a certain accuracy is achieved, whichever occurs first.
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        
        # Refine the corners of the cards
        corners =np.int0(cv.cornerSubPix(component.mask, np.float32(coordinates[:, 0]), (5, 5), (-1, -1), criteria))
        
        quadrilateral = Quadrilateral(component.centroid, contours[0], corners)
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
    quadrilateral.verticesCoords = coord_src

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

def findBestTemplateMatch(possibleCard):
    bestMatchValue = None
    bestMatchRank = None
    bestMatchSuit = None

    possibleCard = util.identifyRankAndSuit(possibleCard)
    if possibleCard == None:
        return None, bestMatchValue
   
    possibleRank, possibleSuit = possibleCard
    
    for templateCardRank in templateCardsRanks:
        
        res = cv.matchTemplate(possibleRank, templateCardRank.img,  cv.TM_CCORR_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)
        
        val = max_val
        if (bestMatchValue == None or val > bestMatchValue) and val >= MIN_MATCH_FOR_TEMPLATE:
            bestMatchValue = val
            bestMatchRank = templateCardRank.name
    
    
    if bestMatchRank == None:
        return None, bestMatchValue
    
    bestMatchValue = None
    
    for templateCardSuit in templateCardsSuits:

        res = cv.matchTemplate(possibleSuit, templateCardSuit.img,  cv.TM_CCORR_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)

        val = max_val
        if (bestMatchValue == None or val > bestMatchValue) and val >= MIN_MATCH_FOR_TEMPLATE:
            bestMatchValue = val
            bestMatchSuit = templateCardSuit.name
     
    if bestMatchSuit == None:
        return None, bestMatchValue
    
    return bestMatchRank + bestMatchSuit, bestMatchValue

def templateMatching(possibleCard):    
    imgToCheck = possibleCard.homography

    # get only the symbol of the card
    imgToCheck = util.getRankSuitImgFromCardImg(imgToCheck)
    util.identifyRankAndSuit(imgToCheck)

    matchName, matchValue = findBestTemplateMatch(imgToCheck)
    
    if(matchName != None):
        return Card(possibleCard, matchName)

    return None

def identifyPossibleCards(img, possibleCards):
    identifiedCards = []

    for possibleCard in possibleCards:
        possibleCard.homography = calculateHomographyAndWarpImage(img, possibleCard)
        identifiedCard = templateMatching(possibleCard)
        if identifiedCard != None:
            identifiedCards.append(identifiedCard)
            
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
        xCentroid[0][1].player = 0
        xCentroid[3][1].player = 1
    else:
        xCentroid[0][1].player = 0
        xCentroid[3][1].player = 2
        
        yCentroid[0][1].player = 1
        yCentroid[3][1].player = 3
      
    return detectedCards

# ---------------------------------------------------------------------

def showTextInImg(img, position, text, color):
    font = cv.FONT_HERSHEY_SIMPLEX  
    fontScale = 1
    thickness = 2
    
    img = cv.putText(img, text, position, font, 
                    fontScale, color, thickness, cv.LINE_AA)

def announceRoundWinnerOrLoser(img, text, player, detectedCards):
    winnerOrLoserCard = None
    winnerOrLoserColor = (0, 255, 0)
    
    for detectedCard in detectedCards:
        if detectedCard.player == player:
            winnerOrLoserCard = detectedCard

    if winnerOrLoserCard == None:
        print("Could not show round winner")
        return  
    
    winnerOrLoserCard.quadrilateral.centroid = list(winnerOrLoserCard.quadrilateral.centroid)
    winnerOrLoserCard.quadrilateral.centroid[0] = max(0, winnerOrLoserCard.quadrilateral.centroid[0] - 50)
    
    if text == "LOSER":
        winnerOrLoserColor = (0, 0, 255)
    
    showTextInImg(img, winnerOrLoserCard.quadrilateral.centroid, text, winnerOrLoserColor)
    # draw card border
    cv.drawContours(img, winnerOrLoserCard.quadrilateral.contours, -1, winnerOrLoserColor, 3)

# ===================================MAIN======================================

setUp()

game = gamePackage.Game()
camera = remoteWebCamPackage.RemoteWebCam()

cardsPerRound = game.getCardsPerRound()

gameOver = False
winner = None

while True:
    camera.nextFrame()
    if not camera.validFrame():
        print("Couldn't get video from camera")
        print("Exiting...")
        break
    
    frame = camera.getFrame()
    
    if not gameOver:
        # Where are the cards
        detectedPossibleCards = detectPossibleCards(frame)

        # Which card is which
        detectedCards = identifyPossibleCards(frame, detectedPossibleCards)
        # print(f"Detected Cards: {[[detectedCard.player, detectedCard.name] for detectedCard in detectedCards]}")

        # Only continues processing if there is the right number of cards on the table
        if len(detectedCards) == cardsPerRound:
            # The person that played each card
            detectedCards = associatePlayersWithCards(detectedCards)

            # verify if it is a new round
            if game.isNewRound(detectedCards):
                print(f"New Round: {[[detectedCard.player, detectedCard.name] for detectedCard in detectedCards]}")

                error = game.gameRound(detectedCards)
                if error != None:
                    error.show()
                else:
                    text, roundWinnerOrLoser = game.getRoundWinnerOrLoser()
                    announceRoundWinnerOrLoser(frame, text, roundWinnerOrLoser, detectedCards)

                if game.gameEnded():
                    winner = game.getGameWinner()
                    gameOver = True
                    print(f"\nGame Over! Winner {winner}")
            
                print("\n###############################\n")
            
            # verify if is the same round
            elif game.isSameRound(detectedCards):
                text, roundWinnerOrLoser = game.getRoundWinnerOrLoser()
                announceRoundWinnerOrLoser(frame, text, roundWinnerOrLoser, detectedCards)

    else:
        frame = showTrophy(frame, winner)

    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break
    
cv.destroyAllWindows()
    