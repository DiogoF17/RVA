class WhistGame:
    def __init__(self):
        print("\n=================================")
        print("           WHIST GAME           ")
        print("=================================\n")

        self.numberOfPlayers = self.getNumberOfPlayers()
        
        print("\n*******************************************\n")
        
        print(f"Selected Game: Whist; Number Of Players: {self.numberOfPlayers}\n")
        
        self.lastRound = []
        self.roundWinner = None

    def getNumberOfPlayers(self):
        while True:
            inputNumberOfPlayers = input("Number Of Players (2 or 4): ")
            
            if not inputNumberOfPlayers.isnumeric():
                print(f"Invalid Number Of Players: {self.numberOfPlayers}, should be either 2 or 4")
                continue

            self.numberOfPlayers = int(inputNumberOfPlayers)
            if self.validNumberOfPlayers(self.numberOfPlayers):
                break

            print(f"Invalid Number Of Players: {self.numberOfPlayers}, should be either 2 or 4")

    def getCardsPerRound(self):
        return self.numberOfPlayers

    def validNumberOfPlayers(self, numberOfPlayers):
        return numberOfPlayers == 2 or numberOfPlayers == 4
        
    def gameRound(self, round):
        if not self.isNewRound(round):
            return
        
        self.detectRoundWinner()
        self.updatePlayersScore()
        self.addPlayedRound(round)
        
    def isNewRound(self, round):
        if len(round) != self.numberOfPlayers:
            return False
        
        for card in round:
            if card in self.lastRound:
                return False
        
        return True
    
    def detectRoundWinner(self, round):
        pass
    
    def updatePlayersScore(self):
        pass
    
    def addPlayedRound(self, round):
        self.lastRound = round
        
    def getRoundWinner(self):
        return "ace"

    def gameEnded(self):
        return False