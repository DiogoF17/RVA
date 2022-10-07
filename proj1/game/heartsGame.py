import game.cards as cards

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
        self.roundWinner = None

    def getCardsPerRound(self):
        return self.numberOfPlayers
        
    def gameRound(self, round):
        cardsNames = [card.name for card in round]
        
        if not self.isNewRound(cardsNames):
            return
        
        if self.isFirstRound() and not self.isValidRound(cardsNames):
            exit("ERROR! Can't play any Hearts of the Queen of Spades in the first round")
        
        self.detectRoundWinner(round)
        self.updatePlayersScore(round)
        self.addPlayedRound(round)
        
    def isNewRound(self, round):
        if len(round) != self.numberOfPlayers:
            return False
        
        for card in round:
            if card in self.lastRound:
                return False
        
        return True     
    
    def isValidRound(self, round):
        for card in round:
            suit = cards.getCardSuit(card)
            if suit == "HEARTS" or card == cards.QUEEN_SPADES:
                return False
            
        return True
    
    def detectRoundWinner(self, round):        
        ownerOfTheGreatestCard, greatestCard = self.resolveRoundStart(round)
        suitOfGreatestCard = cards.getCardSuit(ownerOfTheGreatestCard)
        
        currentPlayer = ownerOfTheGreatestCard
        for i in range(1, self.numberOfPlayers - 1):
            currentPlayer = (currentPlayer + 1) % self.numberOfPlayers
            currentPlayerCard = self.detectPlayerCard(currentPlayer)
            
            suitOfCurrentCard = cards.getCardSuit(currentPlayerCard)
            if suitOfGreatestCard == suitOfCurrentCard and cards[currentPlayerCard]["number"] > cards[greatestCard]["number"]:
                ownerOfTheGreatestCard = currentPlayer
                greatestCard = currentPlayerCard
                suitOfGreatestCard = suitOfCurrentCard
            
        self.roundWinner = ownerOfTheGreatestCard
        print(f"Round Winner: Player {self.roundWinner} | {greatestCard}")
    
    def resolveRoundStart(self, round, cardsNames):
        # it's not the first round of the game
        if not self.isFirstRound():
            player = self.roundWinner
            card = self.detectPlayerCard(player, round)
        # it's the first round but i doesn't start with a 2 of clubs
        elif cards.TWO_CLUBS not in cardsNames:
            exit("ERROR! The Hearts game must start with the 2 of clubs, but it was not detected")
        # it's the first round of the game
        else:
            card = cards.TWO_CLUBS
            player = round[cards.TWO_CLUBS]
            
        return (player, card)
    
    def isFirstRound(self):
        return self.roundWinner == None
    
    def detectPlayerCard(self, player, round):
        for card in round:
            if card.player == player:
                return card
            
        exit(f"ERROR! Couldn't determine player {player} card")
    
    def updatePlayersScore(self, round):
        scoreOnTheTable = self.computeScoreOnRound(round)
        print(f"Score On The Table: {scoreOnTheTable}")
        
    
    def computeScoreOnRound(self, round):
        score = 0
        
        for card in round:
            score += cardsRules[card]["value"]
            
        return score
    
    def addPlayedRound(self, round):
        self.lastRound = round
        
    def getRoundWinner(self):
        return self.roundWinner

    def gameEnded(self):
        return False