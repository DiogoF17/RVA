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
from ar.augmentedReality import showTrophy

# =============================GLOBAL VARIABLES================================

templateCardsRanks = []
templateCardsSuits = []

QUIT_KEY = ord("q")

MIN_AREA_OF_CARDS = 5000
MIN_MATCH_FOR_TEMPLATE = 0.8

# ===============================FUNCTIONS=====================================

def setUp():
    print("\nSetting up...")
    
    # load ranks template
    for fileName in cards.templateCardsRanks:
        img = cv.imread(fileName,0)
        templateCardsRanks.append(templateCard.TemplateCard(cards.templateCardsRanks[fileName], img, None))
        
    # load suit template
    for fileName in cards.templateCardsSuits:
        img = cv.imread(fileName,0)
        templateCardsSuits.append(templateCard.TemplateCard(cards.templateCardsSuits[fileName], img, None))
    
    print("Set up Completed!\n")

# ---------------------------------------------------------------------

def binarize(img, thresholdValue = 127):
    grayScaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binarized = cv.threshold(grayScaleImg, thresholdValue, 255, cv.THRESH_BINARY)
    return binarized

def detectConnectedComponents(img):
    numLabels, labels, stats, centroids = cv.connectedComponentsWithStats(img)
    
    connectedComponents = []
    for i in range(1, numLabels):
        # we assumed that a candidate card must had a minimum area       
        if stats[i, cv.CC_STAT_AREA] >= MIN_AREA_OF_CARDS:
            componentMask = (labels == i).astype("uint8") * 255
            connectedComponent = ConnectedComponent(componentMask, centroids[i])
            connectedComponents.append(connectedComponent)
    
    return connectedComponents

def detectQuadrilaterals(components):
    quadrilaterals = []
    
    for component in components:
        contours, _ = cv.findContours(image=component.mask, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
        coordinates = cv.approxPolyDP(contours[0], 0.04 * cv.arcLength(contours[0], True), True)

        # a card must be quadrilateral
        if len(coordinates) != 4:
            continue
        
        # refine quadrilateral coords
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
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
    # its necessary to order the quadrilateral vertices to 
    # make a correct transformation to be in frontal pose
    coord_src = np.array(util.orderCoordinates(quadrilateral))
    quadrilateral.verticesCoords = coord_src

    # calculate homography to put quadrilateral in frontal pose
    homography, _ = cv.findHomography(coord_src, coord_dst)
    
    # applied homography to the quadrilateral
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
        return None
   
    possibleRank, possibleSuit = possibleCard
    
    # tries to identify the rank of the specified card
    for templateCardRank in templateCardsRanks:
        
        res = cv.matchTemplate(possibleRank, templateCardRank.img,  cv.TM_CCORR_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)
        
        val = max_val
        if (bestMatchValue == None or val > bestMatchValue) and val >= MIN_MATCH_FOR_TEMPLATE:
            bestMatchValue = val
            bestMatchRank = templateCardRank.name
    
    # couldn't determine the rank of the specified card
    if bestMatchRank == None:
        return None
    
    bestMatchValue = None
    
    # tries to identify the suit of the specified card
    for templateCardSuit in templateCardsSuits:

        res = cv.matchTemplate(possibleSuit, templateCardSuit.img,  cv.TM_CCORR_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(res)

        val = max_val
        if (bestMatchValue == None or val > bestMatchValue) and val >= MIN_MATCH_FOR_TEMPLATE:
            bestMatchValue = val
            bestMatchSuit = templateCardSuit.name
    
    # couldn't determine the suit of the specified card
    if bestMatchSuit == None:
        return None
    
    return bestMatchRank + bestMatchSuit

def templateMatching(possibleCard):
    # card in frontal pose
    imgToCheck = possibleCard.homography

    # get only the symbol (rank + suit) of the card
    imgToCheck = util.getRankSuitImgFromCardImg(imgToCheck)

    # identifies card
    matchName = findBestTemplateMatch(imgToCheck)

    return None if matchName == None else Card(possibleCard, matchName)

def identifyPossibleCards(img, possibleCards):
    identifiedCards = []

    # goes through each detected card and tries to identify it
    for possibleCard in possibleCards:
        # gets the card in frontal pose
        possibleCard.homography = calculateHomographyAndWarpImage(img, possibleCard)
        
        # applies templateMatching in order to identify the card
        identifiedCard = templateMatching(possibleCard)
        if identifiedCard != None:
            identifiedCards.append(identifiedCard)
            
    return identifiedCards

# ---------------------------------------------------------------------
def associatePlayersWithCards(detectedCards):
    # tries to assign to each player a card according to card centroids
    # ---------------------------------
    # With 4 players
    #             Player 1 
    #  Player 0               Player 2
    #             Player 3
    # ---------------------------------
    # With 2 players
    #  Player 0              Player 1
    # ---------------------------------

    xCentroid = []
    yCentroid = []
    
    for detectedCard in detectedCards:
        xCentroid.append([detectedCard.quadrilateral.centroid[0],detectedCard])
        yCentroid.append([detectedCard.quadrilateral.centroid[1],detectedCard])
    
    # sort according to X value
    xCentroid.sort(key=(lambda x : x[0]))
    # sort according to Y value
    yCentroid.sort(key=(lambda x : x[0]))
    
    if len(detectedCards) == 2:
        # most left card is the one with lowest X
        # assigned to player 0
        xCentroid[0][1].player = 0

        # most right card is the one with highest X
        # assigned to player 1
        xCentroid[3][1].player = 1
    else:
        # most left card is the one with lowest X
        # assigned to player 0
        xCentroid[0][1].player = 0

        # most right card is the one with highest X
        # assigned to player 2
        xCentroid[3][1].player = 2
        
        # most upper card is the one with lowest Y
        # assigned to player 1
        yCentroid[0][1].player = 1

        # most lower card is the one with highest Y
        # assigned to player 3
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
    
    # gets the losing card
    for detectedCard in detectedCards:
        if detectedCard.player == player:
            winnerOrLoserCard = detectedCard

    if winnerOrLoserCard == None:
        # print("Could not show round winner")
        return  
    
    # gets the centroid of the card
    winnerOrLoserCard.quadrilateral.centroid = list(winnerOrLoserCard.quadrilateral.centroid)
    # moves X a bit to the left in order to the text being centered
    winnerOrLoserCard.quadrilateral.centroid[0] = max(0, winnerOrLoserCard.quadrilateral.centroid[0] - 50)
    
    # if there is a loser in the round the text will be red
    if text == "LOSER":
        winnerOrLoserColor = (0, 0, 255)
    
    # shows winner or loser text on the top of the card
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

    # Where are the cards
    detectedPossibleCards = detectPossibleCards(frame)

    # Which card is which
    detectedCards = identifyPossibleCards(frame, detectedPossibleCards)

    # Only continues processing if there is the right number of cards on the table
    if len(detectedCards) == cardsPerRound:
        # The person that played each card
        detectedCards = associatePlayersWithCards(detectedCards)
        
        # verify if it is a new round
        if game.isNewRound(detectedCards) and not gameOver:
            print(f"New Round: {[[detectedCard.player, detectedCard.name] for detectedCard in detectedCards]}\n")

            error = game.gameRound(detectedCards)
            if error != None:
                error.show()
            else:
                text, roundWinnerOrLoser = game.getRoundWinnerOrLoser()
                announceRoundWinnerOrLoser(frame, text, roundWinnerOrLoser, detectedCards)

            print("\n*******************************************\n")

            if game.gameEnded():
                gameOver = True

                winner = game.getGameWinner()
                print(f"GAME OVER!!!\nWinner: Player {winner}")
        
        # verify if is the same round
        elif game.isSameRound(detectedCards):
            text, roundWinnerOrLoser = game.getRoundWinnerOrLoser()
            announceRoundWinnerOrLoser(frame, text, roundWinnerOrLoser, detectedCards)
    
    if gameOver:
        frame = showTrophy(frame, winner)

    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break
    
cv.destroyAllWindows()
    