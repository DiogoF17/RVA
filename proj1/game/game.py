import game.heartsGame as heartsGame
import game.whistGame as whistGame

class Game:
    def __init__(self):
        self.game = self.getGame()

    def getGame(self):
        print("=================================")
        print("           SELECT GAME           ")
        print("=================================")

        print("\n1) Whist Game")
        print("2) Hearts Game\n")

        option = -1
        while True:
            option = input("Option: ")

            if not option.isnumeric():
                print("Invalid Option!")
                continue

            option = int(option)
            if self.validOption(option, 2):
                break

            print("Invalid Option!")

        return whistGame.WhistGame() if option == 1 else heartsGame.HeartsGame()

    def validOption(self, option, maxValue):
        return option >= 1 and option <= maxValue

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