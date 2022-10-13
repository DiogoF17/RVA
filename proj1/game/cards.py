ACE_HEARTS = "Ace of Hearts"
ACE = "Ace"
TWO = "Two"
THREE = "Three"
FOUR = "Four"
FIVE = "Five"
SIX = "Six"
SEVEN = "Seven"
EIGHT = "Eight"
NINE = "Nine"
TEN = "Ten"
QUEEN = "Queen"
JACK = "Jack"
KING = "King"

SPADES = " of Spades"
HEARTS = " of Hearts"
DIAMONDS = " of Diamonds"
CLUBS = " of Clubs"


def getCardSuit(card):
    return card.split(" ")[-1].upper()
# -------------------------------------------------------------------------

templateCardsRanks = {"./ranks/ace.jpg": ACE,
              "./ranks/two.jpg": TWO,
              "./ranks/three.jpg": THREE,
              "./ranks/four.jpg": FOUR,
              "./ranks/five.jpg": FIVE,
              "./ranks/six.jpg": SIX,
              "./ranks/seven.jpg": SEVEN,
              "./ranks/eight.jpg": EIGHT,
              "./ranks/nine.jpg": NINE,
              "./ranks/ten.jpg": TEN,
              "./ranks/queen.jpg": QUEEN,
              "./ranks/jack.jpg": JACK,
              "./ranks/king.jpg": KING}

templateCardsSuits = {"./suits/spades.jpg": SPADES,
              "./suits/hearts.jpg": HEARTS,
              "./suits/diamonds.jpg": DIAMONDS,
              "./suits/clubs.jpg": CLUBS}