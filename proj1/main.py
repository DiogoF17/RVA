import cv2 as cv
import game.game as gamePackage
import camera.remoteWebCam as remoteWebCamPackage

def binarize(img, thresholdValue = 127):
    binarized = cv.threshold(img, thresholdValue, 255, cv.THRESH_BINARY)
    return binarized

def detectConnectedComponents(img):
    return img

def detectContours(img):
    return img

def detectQuadrilaterals(img):
    return img

# return: img with only the cards
def detectCards(img):
    binarized = binarize(img)
    connectedComponents = detectConnectedComponents(binarized)
    contours = detectContours(connectedComponents)
    cards = detectQuadrilaterals(contours)
    
    return cards

# return: {cardName: img}
def identifyCards(cards):
    return []

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

QUIT_KEY = ord("q")

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
    cards = detectCards(frame)
    # # Which card is which
    # cardsNames = identifyCards(cards)
    # # The person that played each card
    # playersAssociatedWithEachCard = associatePlayersWithCards(cardsNames)

    # game.gameRound(playersAssociatedWithEachCard)
    # roundWinner = game.getRoundWinner()
    
    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    if key == QUIT_KEY:
        break
    
cv.destroyAllWindows()
    
