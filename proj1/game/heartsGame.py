import game.cards as cards
from utils.error import Error

cardsRules = {cards.TWO_CLUBS: {"number": 1, "value": 0},
              cards.THREE_CLUBS: {"number": 2, "value": 0},
              cards.FOUR_CLUBS: {"number": 3, "value": 0},
              cards.FIVE_CLUBS: {"number": 4, "value": 0},
              cards.SIX_CLUBS: {"number": 5, "value": 0},
              cards.SEVEN_CLUBS: {"number": 6, "value": 0},
              cards.EIGHT_CLUBS: {"number": 7, "value": 0},
              cards.NINE_CLUBS: {"number": 8, "value": 0},
              cards.TEN_CLUBS: {"number": 9, "value": 0},
              cards.QUEEN_CLUBS: {"number": 10, "value": 0},
              cards.JACK_CLUBS: {"number": 11, "value": 0},
              cards.KING_CLUBS: {"number": 12, "value": 0},
              cards.ACE_CLUBS: {"number": 13, "value": 0},
              cards.TWO_SPADES: {"number": 1, "value": 0},
              cards.THREE_SPADES: {"number": 2, "value": 0},
              cards.FOUR_SPADES: {"number": 3, "value": 0},
              cards.FIVE_SPADES: {"number": 4, "value": 0},
              cards.SIX_SPADES: {"number": 5, "value": 0},
              cards.SEVEN_SPADES: {"number": 6, "value": 0},
              cards.EIGHT_SPADES: {"number": 7, "value": 0},
              cards.NINE_SPADES: {"number": 8, "value": 0},
              cards.TEN_SPADES: {"number": 9, "value": 0},
              cards.QUEEN_SPADES: {"number": 10, "value": 13},
              cards.JACK_SPADES: {"number": 11, "value": 0},
              cards.KING_SPADES: {"number": 12, "value": 0},
              cards.ACE_SPADES: {"number": 13, "value": 0},
              cards.TWO_DIAMONDS: {"number": 1, "value": 0},
              cards.THREE_DIAMONDS: {"number": 2, "value": 0},
              cards.FOUR_DIAMONDS: {"number": 3, "value": 0},
              cards.FIVE_DIAMONDS: {"number": 4, "value": 0},
              cards.SIX_DIAMONDS: {"number": 5, "value": 0},
              cards.SEVEN_DIAMONDS: {"number": 6, "value": 0},
              cards.EIGHT_DIAMONDS: {"number": 7, "value": 0},
              cards.NINE_DIAMONDS: {"number": 8, "value": 0},
              cards.TEN_DIAMONDS: {"number": 9, "value": 0},
              cards.QUEEN_DIAMONDS: {"number": 10, "value": 0},
              cards.JACK_DIAMONDS: {"number": 11, "value": 0},
              cards.KING_DIAMONDS: {"number": 12, "value": 0},
              cards.ACE_DIAMONDS: {"number": 13, "value": 0},
              cards.TWO_HEARTS: {"number": 1, "value": 1},
              cards.THREE_HEARTS: {"number": 2, "value": 1},
              cards.FOUR_HEARTS: {"number": 3, "value": 1},
              cards.FIVE_HEARTS: {"number": 4, "value": 1},
              cards.SIX_HEARTS: {"number": 5, "value": 1},
              cards.SEVEN_HEARTS: {"number": 6, "value": 1},
              cards.EIGHT_HEARTS: {"number": 7, "value": 1},
              cards.NINE_HEARTS: {"number": 8, "value": 1},
              cards.TEN_HEARTS: {"number": 9, "value": 1},
              cards.QUEEN_HEARTS: {"number": 10, "value": 1},
              cards.JACK_HEARTS: {"number": 11, "value": 1},
              cards.KING_HEARTS: {"number": 12, "value": 1},
              cards.ACE_HEARTS: {"number": 13, "value": 1}}

class HeartsGame:
    def __init__(self):
        print("\n=================================")
        print("           HEARTS GAME           ")
        print("=================================\n")

        self.numberOfPlayers = 4
        
        print("\n*******************************************\n")
        
        print("Selected Game: Hearts; Number Of Players: 4\n")
        
        self.lastRound = []
        self.roundLoser = None
        self.score = {0: 0, 1: 0, 2: 0, 3: 0}

    def getCardsPerRound(self):
        return self.numberOfPlayers
        
    def gameRound(self, round):
        cardsNames = [card.name for card in round]
        
        if self.isFirstRound() and not self.isValidRound(cardsNames):
            return Error("ERROR! Can't play any Hearts or the Queen of Spades in the first round")
        
        error = self.detectRoundLoser(round, cardsNames)
        if error != None:
            return error

        self.updatePlayersScore(cardsNames)
        self.addPlayedRound(cardsNames)

        return None
        
    def isNewRound(self, round):
        if len(round) != self.numberOfPlayers:
            return False
        
        for card in round:
            if card.name in self.lastRound:
                return False
        
        return True

    def isSameRound(self, round):        
        for card in round:
            if not card.name in self.lastRound:
                return False
        
        return True
    
    def isValidRound(self, cardsNames):
        for card in cardsNames:
            suit = cards.getCardSuit(card)
            if suit == "HEARTS" or card == cards.QUEEN_SPADES:
                return False
            
        return True
    
    def detectRoundLoser(self, round, cardsNames):        
        roundStart = self.resolveRoundStart(round, cardsNames)
        if isinstance(roundStart, Error):
            return roundStart

        ownerOfTheGreatestCard, greatestCard = roundStart
        suitOfGreatestCard = cards.getCardSuit(greatestCard)
        
        currentPlayer = ownerOfTheGreatestCard
        for _ in range(self.numberOfPlayers - 1):
            currentPlayer = (currentPlayer + 1) % self.numberOfPlayers
            currentPlayerCard = self.detectPlayerCard(currentPlayer, round)
            if isinstance(currentPlayerCard, Error):
                return currentPlayerCard
            
            suitOfCurrentCard = cards.getCardSuit(currentPlayerCard)

            if suitOfGreatestCard == suitOfCurrentCard and cardsRules[currentPlayerCard]["number"] > cardsRules[greatestCard]["number"]:
                ownerOfTheGreatestCard = currentPlayer
                greatestCard = currentPlayerCard
                suitOfGreatestCard = suitOfCurrentCard
            
        self.roundLoser = ownerOfTheGreatestCard
        print(f"Round Loser: Player {self.roundLoser} | {greatestCard}")

        return None
    
    def resolveRoundStart(self, round, cardsNames):
        # it's not the first round of the game
        if not self.isFirstRound():
            player = self.roundLoser
            card = self.detectPlayerCard(player, round)
            if isinstance(card, Error):
                return card
        # it's the first round but i doesn't start with a 2 of clubs
        elif cards.TWO_CLUBS not in cardsNames:
            return Error("The Hearts game must start with the 2 of clubs, but it was not detected")
        # it's the first round of the game
        else:
            card = cards.TWO_CLUBS
            player = self.detectPlayerOfCard(cards.TWO_CLUBS, round)
            if isinstance(player, Error):
                return player
            
        return (player, card)
    
    def isFirstRound(self):
        return self.roundLoser == None
    
    def detectPlayerCard(self, player, round):
        for card in round:
            if card.player == player:
                return card.name
            
        return Error(f"ERROR! Couldn't determine player {player} card")

    def detectPlayerOfCard(self, cardName, round):
        for card in round:
            if card.name == cardName:
                return card.player
            
        return Error(f"ERROR! Couldn't determine player of {cardName}")
    
    def updatePlayersScore(self, cardsNames):
        scoreOnTheTable = self.computeScoreOnRound(cardsNames)
        self.score[self.roundLoser] += scoreOnTheTable

        print(f"Score On The Table: {scoreOnTheTable}")
    
    def computeScoreOnRound(self, cardsNames):
        score = 0
        
        for cardName in cardsNames:
            score += cardsRules[cardName]["value"]
            
        return score
    
    def addPlayedRound(self, cardsNames):
        self.lastRound = cardsNames
        
    def getRoundLoser(self):
        return self.roundLoser

    def gameEnded(self):
        for player in self.score:
            if self.score[player] >= 100:
                return True

        return False

    def getGameWinner(self):
        lowestScore = 1000 # very high number
        playerWithLowestScore = None

        for player in self.score:
            if self.score[player] < lowestScore:
                lowestScore = self.score[player]
                playerWithLowestScore = player

        return playerWithLowestScore