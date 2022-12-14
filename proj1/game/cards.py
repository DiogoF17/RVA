ACE_HEARTS = "Ace of Hearts"
TWO_HEARTS = "Two of Hearts"
THREE_HEARTS = "Three of Hearts"
FOUR_HEARTS = "Four of Hearts"
FIVE_HEARTS = "Five of Hearts"
SIX_HEARTS = "Six of Hearts"
SEVEN_HEARTS = "Seven of Hearts"
EIGHT_HEARTS = "Eight of Hearts"
NINE_HEARTS = "Nine of Hearts"
TEN_HEARTS = "Ten of Hearts"
QUEEN_HEARTS = "Queen of Hearts"
JACK_HEARTS = "Jack of Hearts"
KING_HEARTS = "King of Hearts"

ACE_DIAMONDS = "Ace of Diamonds"
TWO_DIAMONDS = "Two of Diamonds"
THREE_DIAMONDS = "Three of Diamonds"
FOUR_DIAMONDS = "Four of Diamonds"
FIVE_DIAMONDS = "Five of Diamonds"
SIX_DIAMONDS = "Six of Diamonds"
SEVEN_DIAMONDS = "Seven of Diamonds"
EIGHT_DIAMONDS = "Eight of Diamonds"
NINE_DIAMONDS = "Nine of Diamonds"
TEN_DIAMONDS = "Ten of Diamonds"
QUEEN_DIAMONDS = "Queen of Diamonds"
JACK_DIAMONDS = "Jack of Diamonds"
KING_DIAMONDS = "King of Diamonds"

ACE_CLUBS = "Ace of Clubs"
TWO_CLUBS = "Two of Clubs"
THREE_CLUBS = "Three of Clubs"
FOUR_CLUBS = "Four of Clubs"
FIVE_CLUBS = "Five of Clubs"
SIX_CLUBS = "Six of Clubs"
SEVEN_CLUBS = "Seven of Clubs"
EIGHT_CLUBS = "Eight of Clubs"
NINE_CLUBS = "Nine of Clubs"
TEN_CLUBS = "Ten of Clubs"
QUEEN_CLUBS = "Queen of Clubs"
JACK_CLUBS = "Jack of Clubs"
KING_CLUBS = "King of Clubs"

ACE_SPADES = "Ace of Spades"
TWO_SPADES = "Two of Spades"
THREE_SPADES = "Three of Spades"
FOUR_SPADES = "Four of Spades"
FIVE_SPADES = "Five of Spades"
SIX_SPADES = "Six of Spades"
SEVEN_SPADES = "Seven of Spades"
EIGHT_SPADES = "Eight of Spades"
NINE_SPADES = "Nine of Spades"
TEN_SPADES = "Ten of Spades"
QUEEN_SPADES = "Queen of Spades"
JACK_SPADES = "Jack of Spades"
KING_SPADES = "King of Spades"

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