import game.heartsGame as heartsGame

class Game:
    def __init__(self):
        self.game = self.getGame()

    def getGame(self):
        print("=================================")
        print("           SELECT GAME           ")
        print("=================================")

        print("\n1) Hearts Game")
        print("0) Exit\n")

        option = -1
        while True:
            option = input("Option: ")

            if not option.isnumeric():
                print("Invalid Option!")
                continue

            option = int(option)
            if self.validOption(option, 1):
                break

            print("Invalid Option!")

        if option == 0:
            exit()

        return heartsGame.HeartsGame()

    def validOption(self, option, maxValue):
        return option >= 0 and option <= maxValue

    def getCardsPerRound(self):
        return self.game.getCardsPerRound()

    def isNewRound(self, round):
        return self.game.isNewRound(round)

    def isSameRound(self, round):        
        return self.game.isSameRound(round)

    def gameRound(self, cards):
        return self.game.gameRound(cards)
        
    def getRoundWinnerOrLoser(self):
        if isinstance(self.game, heartsGame.HeartsGame):
            return "LOSER", self.game.getRoundLoser()
        else:
            return "WINNER", self.game.getRoundWinner()

    def gameEnded(self):
        return self.game.gameEnded()
    
    def getGameWinner(self):
        return self.game.getGameWinner()