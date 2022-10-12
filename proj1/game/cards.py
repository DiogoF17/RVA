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

# templateCards = {"./cards_normal/1.jpg": ACE_SPADES,
#               "./cards_normal/2.jpg": ACE_HEARTS,
#               "./cards_normal/3.jpg": ACE_CLUBS,
#               "./cards_normal/4.jpg": ACE_DIAMONDS,
#               "./cards_normal/1B.jpg": ACE_SPADES,
#               "./cards_normal/2B.jpg": ACE_HEARTS,
#               "./cards_normal/3B.jpg": ACE_CLUBS,
#               "./cards_normal/4B.jpg": ACE_DIAMONDS,
#               "./cards_normal/5.jpg": TWO_SPADES,
#               "./cards_normal/6.jpg": TWO_HEARTS,
#               "./cards_normal/7.jpg": TWO_CLUBS,
#               "./cards_normal/8.jpg": TWO_DIAMONDS,
#               "./cards_normal/9.jpg": THREE_SPADES,
#               "./cards_normal/10.jpg": THREE_HEARTS,
#               "./cards_normal/11.jpg": THREE_CLUBS,
#               "./cards_normal/12.jpg": THREE_DIAMONDS,
#               "./cards_normal/13.jpg": FOUR_SPADES,
#               "./cards_normal/14.jpg": FOUR_HEARTS,
#               "./cards_normal/15.jpg": FOUR_CLUBS,
#               "./cards_normal/16.jpg": FOUR_DIAMONDS,
#               "./cards_normal/17.jpg": FIVE_SPADES,
#               "./cards_normal/18.jpg": FIVE_HEARTS,
#               "./cards_normal/19.jpg": FIVE_CLUBS,
#               "./cards_normal/20.jpg": FIVE_DIAMONDS,
#               "./cards_normal/21.jpg": SIX_SPADES,
#               "./cards_normal/22.jpg": SIX_HEARTS,
#               "./cards_normal/23.jpg": SIX_CLUBS,
#               "./cards_normal/24.jpg": SIX_DIAMONDS,
#               "./cards_normal/25.jpg": SEVEN_SPADES,
#               "./cards_normal/26.jpg": SEVEN_HEARTS,
#               "./cards_normal/27.jpg": SEVEN_CLUBS,
#               "./cards_normal/28.jpg": SEVEN_DIAMONDS,
#               "./cards_normal/29.jpg": EIGHT_SPADES,
#               "./cards_normal/30.jpg": EIGHT_HEARTS,
#               "./cards_normal/31.jpg": EIGHT_CLUBS,
#               "./cards_normal/32.jpg": EIGHT_DIAMONDS,
#               "./cards_normal/33.jpg": NINE_SPADES,
#               "./cards_normal/34.jpg": NINE_HEARTS,
#               "./cards_normal/35.jpg": NINE_CLUBS,
#               "./cards_normal/36.jpg": NINE_DIAMONDS,
#               "./cards_normal/37.jpg": TEN_SPADES,
#               "./cards_normal/38.jpg": TEN_HEARTS,
#               "./cards_normal/39.jpg": TEN_CLUBS,
#               "./cards_normal/40.jpg": TEN_DIAMONDS,
#               "./cards_normal/41.jpg": QUEEN_SPADES,
#               "./cards_normal/42.jpg": QUEEN_HEARTS,
#               "./cards_normal/43.jpg": QUEEN_CLUBS,
#               "./cards_normal/44.jpg": QUEEN_DIAMONDS,
#               "./cards_normal/45.jpg": JACK_SPADES,
#               "./cards_normal/46.jpg": JACK_HEARTS,
#               "./cards_normal/47.jpg": JACK_CLUBS,
#               "./cards_normal/48.jpg": JACK_DIAMONDS,
#               "./cards_normal/49.jpg": KING_SPADES,
#               "./cards_normal/50.jpg": KING_HEARTS,
#               "./cards_normal/51.jpg": KING_CLUBS,
#               "./cards_normal/52.jpg": KING_DIAMONDS,
#               "./cards_normal/1Rotated.jpg": ACE_SPADES,
#               "./cards_normal/2Rotated.jpg": ACE_HEARTS,
#               "./cards_normal/3Rotated.jpg": ACE_CLUBS,
#               "./cards_normal/4Rotated.jpg": ACE_DIAMONDS,
#               "./cards_normal/1BRotated.jpg": ACE_SPADES,
#               "./cards_normal/2BRotated.jpg": ACE_HEARTS,
#               "./cards_normal/3BRotated.jpg": ACE_CLUBS,
#               "./cards_normal/4BRotated.jpg": ACE_DIAMONDS,
#               "./cards_normal/5Rotated.jpg": TWO_SPADES,
#               "./cards_normal/6Rotated.jpg": TWO_HEARTS,
#               "./cards_normal/7Rotated.jpg": TWO_CLUBS,
#               "./cards_normal/8Rotated.jpg": TWO_DIAMONDS,
#               "./cards_normal/9Rotated.jpg": THREE_SPADES,
#               "./cards_normal/10Rotated.jpg": THREE_HEARTS,
#               "./cards_normal/11Rotated.jpg": THREE_CLUBS,
#               "./cards_normal/12Rotated.jpg": THREE_DIAMONDS,
#               "./cards_normal/13Rotated.jpg": FOUR_SPADES,
#               "./cards_normal/14Rotated.jpg": FOUR_HEARTS,
#               "./cards_normal/15Rotated.jpg": FOUR_CLUBS,
#               "./cards_normal/16Rotated.jpg": FOUR_DIAMONDS,
#               "./cards_normal/17Rotated.jpg": FIVE_SPADES,
#               "./cards_normal/18Rotated.jpg": FIVE_HEARTS,
#               "./cards_normal/19Rotated.jpg": FIVE_CLUBS,
#               "./cards_normal/20Rotated.jpg": FIVE_DIAMONDS,
#               "./cards_normal/21Rotated.jpg": SIX_SPADES,
#               "./cards_normal/22Rotated.jpg": SIX_HEARTS,
#               "./cards_normal/23Rotated.jpg": SIX_CLUBS,
#               "./cards_normal/24Rotated.jpg": SIX_DIAMONDS,
#               "./cards_normal/25Rotated.jpg": SEVEN_SPADES,
#               "./cards_normal/26Rotated.jpg": SEVEN_HEARTS,
#               "./cards_normal/27Rotated.jpg": SEVEN_CLUBS,
#               "./cards_normal/28Rotated.jpg": SEVEN_DIAMONDS,
#               "./cards_normal/29Rotated.jpg": EIGHT_SPADES,
#               "./cards_normal/30Rotated.jpg": EIGHT_HEARTS,
#               "./cards_normal/31Rotated.jpg": EIGHT_CLUBS,
#               "./cards_normal/32Rotated.jpg": EIGHT_DIAMONDS,
#               "./cards_normal/33Rotated.jpg": NINE_SPADES,
#               "./cards_normal/34Rotated.jpg": NINE_HEARTS,
#               "./cards_normal/35Rotated.jpg": NINE_CLUBS,
#               "./cards_normal/36Rotated.jpg": NINE_DIAMONDS,
#               "./cards_normal/37Rotated.jpg": TEN_SPADES,
#               "./cards_normal/38Rotated.jpg": TEN_HEARTS,
#               "./cards_normal/39Rotated.jpg": TEN_CLUBS,
#               "./cards_normal/40Rotated.jpg": TEN_DIAMONDS,
#               "./cards_normal/41Rotated.jpg": QUEEN_SPADES,
#               "./cards_normal/42Rotated.jpg": QUEEN_HEARTS,
#               "./cards_normal/43Rotated.jpg": QUEEN_CLUBS,
#               "./cards_normal/44Rotated.jpg": QUEEN_DIAMONDS,
#               "./cards_normal/45Rotated.jpg": JACK_SPADES,
#               "./cards_normal/46Rotated.jpg": JACK_HEARTS,
#               "./cards_normal/47Rotated.jpg": JACK_CLUBS,
#               "./cards_normal/48Rotated.jpg": JACK_DIAMONDS,
#               "./cards_normal/49Rotated.jpg": KING_SPADES,
#               "./cards_normal/50Rotated.jpg": KING_HEARTS,
#               "./cards_normal/51Rotated.jpg": KING_CLUBS,
#               "./cards_normal/52Rotated.jpg": KING_DIAMONDS}

# templateCards = {"./cards_normal/1.jpg": ACE_SPADES,
#               "./cards_normal/2.jpg": ACE_HEARTS,
#               "./cards_normal/3.jpg": ACE_CLUBS,
#               "./cards_normal/4.jpg": ACE_DIAMONDS,
#               "./cards_normal/1B.jpg": ACE_SPADES,
#               "./cards_normal/2B.jpg": ACE_HEARTS,
#               "./cards_normal/3B.jpg": ACE_CLUBS,
#               "./cards_normal/4B.jpg": ACE_DIAMONDS,
#               "./cards_normal/5.jpg": TWO_SPADES,
#               "./cards_normal/6.jpg": TWO_HEARTS,
#               "./cards_normal/7.jpg": TWO_CLUBS,
#               "./cards_normal/8.jpg": TWO_DIAMONDS,
#               "./cards_normal/9.jpg": THREE_SPADES,
#               "./cards_normal/10.jpg": THREE_HEARTS}

# templateCardsSimple = {"./cards_simple/1s.jpg": ACE_SPADES,
#               "./cards_simple/1h.jpg": ACE_HEARTS,
#               "./cards_simple/1c.jpg": ACE_CLUBS,
#               "./cards_simple/1d.jpg": ACE_DIAMONDS,
#               "./cards_simple/1Bs.jpg": ACE_SPADES,
#               "./cards_simple/1Bh.jpg": ACE_HEARTS,
#               "./cards_simple/1Bc.jpg": ACE_CLUBS,
#               "./cards_simple/1Bd.jpg": ACE_DIAMONDS,
#               "./cards_simple/2s.jpg": TWO_SPADES,
#               "./cards_simple/2h.jpg": TWO_HEARTS,
#               "./cards_simple/2c.jpg": TWO_CLUBS,
#               "./cards_simple/2d.jpg": TWO_DIAMONDS,
#               "./cards_simple/3s.jpg": THREE_SPADES,
#               "./cards_simple/3h.jpg": THREE_HEARTS,
#               "./cards_simple/3c.jpg": THREE_CLUBS,
#               "./cards_simple/3d.jpg": THREE_DIAMONDS,
#               "./cards_simple/4s.jpg": FOUR_SPADES,
#               "./cards_simple/4h.jpg": FOUR_HEARTS,
#               "./cards_simple/4c.jpg": FOUR_CLUBS,
#               "./cards_simple/4d.jpg": FOUR_DIAMONDS,
#               "./cards_simple/5s.jpg": FIVE_SPADES,
#               "./cards_simple/5h.jpg": FIVE_HEARTS,
#               "./cards_simple/5c.jpg": FIVE_CLUBS,
#               "./cards_simple/5d.jpg": FIVE_DIAMONDS,
#               "./cards_simple/6s.jpg": SIX_SPADES,
#               "./cards_simple/6h.jpg": SIX_HEARTS,
#               "./cards_simple/6c.jpg": SIX_CLUBS,
#               "./cards_simple/6d.jpg": SIX_DIAMONDS,
#               "./cards_simple/7s.jpg": SEVEN_SPADES,
#               "./cards_simple/7h.jpg": SEVEN_HEARTS,
#               "./cards_simple/7c.jpg": SEVEN_CLUBS,
#               "./cards_simple/7d.jpg": SEVEN_DIAMONDS,
#               "./cards_simple/8s.jpg": EIGHT_SPADES,
#               "./cards_simple/8h.jpg": EIGHT_HEARTS,
#               "./cards_simple/8c.jpg": EIGHT_CLUBS,
#               "./cards_simple/8d.jpg": EIGHT_DIAMONDS,
#               "./cards_simple/9s.jpg": NINE_SPADES,
#               "./cards_simple/9h.jpg": NINE_HEARTS,
#               "./cards_simple/9c.jpg": NINE_CLUBS,
#               "./cards_simple/9d.jpg": NINE_DIAMONDS,
#               "./cards_simple/10s.jpg": TEN_SPADES,
#               "./cards_simple/10h.jpg": TEN_HEARTS,
#               "./cards_simple/10c.jpg": TEN_CLUBS,
#               "./cards_simple/10d.jpg": TEN_DIAMONDS,
#               "./cards_simple/11s.jpg": QUEEN_SPADES,
#               "./cards_simple/11h.jpg": QUEEN_HEARTS,
#               "./cards_simple/11c.jpg": QUEEN_CLUBS,
#               "./cards_simple/11d.jpg": QUEEN_DIAMONDS,
#               "./cards_simple/12s.jpg": JACK_SPADES,
#               "./cards_simple/12h.jpg": JACK_HEARTS,
#               "./cards_simple/12c.jpg": JACK_CLUBS,
#               "./cards_simple/12d.jpg": JACK_DIAMONDS,
#               "./cards_simple/13s.jpg": KING_SPADES,
#               "./cards_simple/13h.jpg": KING_HEARTS,
#               "./cards_simple/13c.jpg": KING_CLUBS,
#               "./cards_simple/13d.jpg": KING_DIAMONDS}


templateCardsRanks = {"./cards_simple_plusplus/ranks/ace.jpg": ACE,
              "./cards_simple_plusplus/ranks/two.jpg": TWO,
              "./cards_simple_plusplus/ranks/three.jpg": THREE,
              "./cards_simple_plusplus/ranks/four.jpg": FOUR,
              "./cards_simple_plusplus/ranks/five.jpg": FIVE,
              "./cards_simple_plusplus/ranks/six.jpg": SIX,
              "./cards_simple_plusplus/ranks/seven.jpg": SEVEN,
              "./cards_simple_plusplus/ranks/eight.jpg": EIGHT,
              "./cards_simple_plusplus/ranks/nine.jpg": NINE,
              "./cards_simple_plusplus/ranks/ten.jpg": TEN,
              "./cards_simple_plusplus/ranks/queen.jpg": QUEEN,
              "./cards_simple_plusplus/ranks/jack.jpg": JACK,
              "./cards_simple_plusplus/ranks/king.jpg": KING}

templateCardsSuits = {"./cards_simple_plusplus/suits/spades.jpg": SPADES,
              "./cards_simple_plusplus/suits/hearts.jpg": HEARTS,
              "./cards_simple_plusplus/suits/diamonds.jpg": DIAMONDS,
              "./cards_simple_plusplus/suits/clubs.jpg": CLUBS}