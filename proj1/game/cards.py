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

def getCardSuit(card):
    return card.split(" ")[-1].upper()
# -------------------------------------------------------------------------

templateCards = {"./cards_normal/1.png": ACE_SPADES,
              "./cards_normal/2.png": ACE_HEARTS,
              "./cards_normal/3.png": ACE_CLUBS,
              "./cards_normal/4.png": ACE_DIAMONDS,
              "./cards_normal/1B.png": ACE_SPADES,
              "./cards_normal/2B.png": ACE_HEARTS,
              "./cards_normal/3B.png": ACE_CLUBS,
              "./cards_normal/4B.png": ACE_DIAMONDS,
              "./cards_normal/5.png": TWO_SPADES,
              "./cards_normal/6.png": TWO_HEARTS,
              "./cards_normal/7.png": TWO_CLUBS,
              "./cards_normal/8.png": TWO_DIAMONDS,
              "./cards_normal/9.png": THREE_SPADES,
              "./cards_normal/10.png": THREE_HEARTS,
              "./cards_normal/11.png": THREE_CLUBS,
              "./cards_normal/12.png": THREE_DIAMONDS,
              "./cards_normal/13.png": FOUR_SPADES,
              "./cards_normal/14.png": FOUR_HEARTS,
              "./cards_normal/15.png": FOUR_CLUBS,
              "./cards_normal/16.png": FOUR_DIAMONDS,
              "./cards_normal/17.png": FIVE_SPADES,
              "./cards_normal/18.png": FIVE_HEARTS,
              "./cards_normal/19.png": FIVE_CLUBS,
              "./cards_normal/20.png": FIVE_DIAMONDS,
              "./cards_normal/21.png": SIX_SPADES,
              "./cards_normal/22.png": SIX_HEARTS,
              "./cards_normal/23.png": SIX_CLUBS,
              "./cards_normal/24.png": SIX_DIAMONDS,
              "./cards_normal/25.png": SEVEN_SPADES,
              "./cards_normal/26.png": SEVEN_HEARTS,
              "./cards_normal/27.png": SEVEN_CLUBS,
              "./cards_normal/28.png": SEVEN_DIAMONDS,
              "./cards_normal/29.png": EIGHT_SPADES,
              "./cards_normal/30.png": EIGHT_HEARTS,
              "./cards_normal/31.png": EIGHT_CLUBS,
              "./cards_normal/32.png": EIGHT_DIAMONDS,
              "./cards_normal/33.png": NINE_SPADES,
              "./cards_normal/34.png": NINE_HEARTS,
              "./cards_normal/35.png": NINE_CLUBS,
              "./cards_normal/36.png": NINE_DIAMONDS,
              "./cards_normal/37.png": TEN_SPADES,
              "./cards_normal/38.png": TEN_HEARTS,
              "./cards_normal/39.png": TEN_CLUBS,
              "./cards_normal/40.png": TEN_DIAMONDS,
              "./cards_normal/41.png": QUEEN_SPADES,
              "./cards_normal/42.png": QUEEN_HEARTS,
              "./cards_normal/43.png": QUEEN_CLUBS,
              "./cards_normal/44.png": QUEEN_DIAMONDS,
              "./cards_normal/45.png": JACK_SPADES,
              "./cards_normal/46.png": JACK_HEARTS,
              "./cards_normal/47.png": JACK_CLUBS,
              "./cards_normal/48.png": JACK_DIAMONDS,
              "./cards_normal/49.png": KING_SPADES,
              "./cards_normal/50.png": KING_HEARTS,
              "./cards_normal/51.png": KING_CLUBS,
              "./cards_normal/52.png": KING_DIAMONDS,
              "./cards_normal/1Rotated.png": ACE_SPADES,
              "./cards_normal/2Rotated.png": ACE_HEARTS,
              "./cards_normal/3Rotated.png": ACE_CLUBS,
              "./cards_normal/4Rotated.png": ACE_DIAMONDS,
              "./cards_normal/1BRotated.png": ACE_SPADES,
              "./cards_normal/2BRotated.png": ACE_HEARTS,
              "./cards_normal/3BRotated.png": ACE_CLUBS,
              "./cards_normal/4BRotated.png": ACE_DIAMONDS,
              "./cards_normal/5Rotated.png": TWO_SPADES,
              "./cards_normal/6Rotated.png": TWO_HEARTS,
              "./cards_normal/7Rotated.png": TWO_CLUBS,
              "./cards_normal/8Rotated.png": TWO_DIAMONDS,
              "./cards_normal/9Rotated.png": THREE_SPADES,
              "./cards_normal/10Rotated.png": THREE_HEARTS,
              "./cards_normal/11Rotated.png": THREE_CLUBS,
              "./cards_normal/12Rotated.png": THREE_DIAMONDS,
              "./cards_normal/13Rotated.png": FOUR_SPADES,
              "./cards_normal/14Rotated.png": FOUR_HEARTS,
              "./cards_normal/15Rotated.png": FOUR_CLUBS,
              "./cards_normal/16Rotated.png": FOUR_DIAMONDS,
              "./cards_normal/17Rotated.png": FIVE_SPADES,
              "./cards_normal/18Rotated.png": FIVE_HEARTS,
              "./cards_normal/19Rotated.png": FIVE_CLUBS,
              "./cards_normal/20Rotated.png": FIVE_DIAMONDS,
              "./cards_normal/21Rotated.png": SIX_SPADES,
              "./cards_normal/22Rotated.png": SIX_HEARTS,
              "./cards_normal/23Rotated.png": SIX_CLUBS,
              "./cards_normal/24Rotated.png": SIX_DIAMONDS,
              "./cards_normal/25Rotated.png": SEVEN_SPADES,
              "./cards_normal/26Rotated.png": SEVEN_HEARTS,
              "./cards_normal/27Rotated.png": SEVEN_CLUBS,
              "./cards_normal/28Rotated.png": SEVEN_DIAMONDS,
              "./cards_normal/29Rotated.png": EIGHT_SPADES,
              "./cards_normal/30Rotated.png": EIGHT_HEARTS,
              "./cards_normal/31Rotated.png": EIGHT_CLUBS,
              "./cards_normal/32Rotated.png": EIGHT_DIAMONDS,
              "./cards_normal/33Rotated.png": NINE_SPADES,
              "./cards_normal/34Rotated.png": NINE_HEARTS,
              "./cards_normal/35Rotated.png": NINE_CLUBS,
              "./cards_normal/36Rotated.png": NINE_DIAMONDS,
              "./cards_normal/37Rotated.png": TEN_SPADES,
              "./cards_normal/38Rotated.png": TEN_HEARTS,
              "./cards_normal/39Rotated.png": TEN_CLUBS,
              "./cards_normal/40Rotated.png": TEN_DIAMONDS,
              "./cards_normal/41Rotated.png": QUEEN_SPADES,
              "./cards_normal/42Rotated.png": QUEEN_HEARTS,
              "./cards_normal/43Rotated.png": QUEEN_CLUBS,
              "./cards_normal/44Rotated.png": QUEEN_DIAMONDS,
              "./cards_normal/45Rotated.png": JACK_SPADES,
              "./cards_normal/46Rotated.png": JACK_HEARTS,
              "./cards_normal/47Rotated.png": JACK_CLUBS,
              "./cards_normal/48Rotated.png": JACK_DIAMONDS,
              "./cards_normal/49Rotated.png": KING_SPADES,
              "./cards_normal/50Rotated.png": KING_HEARTS,
              "./cards_normal/51Rotated.png": KING_CLUBS,
              "./cards_normal/52Rotated.png": KING_DIAMONDS}

templateCardsSimple = {"./cards_simple/1s.jpg": ACE_SPADES,
              "./cards_simple/1h.jpg": ACE_HEARTS,
              "./cards_simple/1c.jpg": ACE_CLUBS,
              "./cards_simple/1d.jpg": ACE_DIAMONDS,
              "./cards_simple/1Bs.png": ACE_SPADES,
              "./cards_simple/1Bh.png": ACE_HEARTS,
              "./cards_simple/1Bc.png": ACE_CLUBS,
              "./cards_simple/1Bd.png": ACE_DIAMONDS,
              "./cards_simple/2s.jpg": TWO_SPADES,
              "./cards_simple/2h.jpg": TWO_HEARTS,
              "./cards_simple/2c.jpg": TWO_CLUBS,
              "./cards_simple/2d.jpg": TWO_DIAMONDS,
              "./cards_simple/3s.jpg": THREE_SPADES,
              "./cards_simple/3h.jpg": THREE_HEARTS,
              "./cards_simple/3c.jpg": THREE_CLUBS,
              "./cards_simple/3d.jpg": THREE_DIAMONDS,
              "./cards_simple/4s.jpg": FOUR_SPADES,
              "./cards_simple/4h.jpg": FOUR_HEARTS,
              "./cards_simple/4c.jpg": FOUR_CLUBS,
              "./cards_simple/4d.jpg": FOUR_DIAMONDS,
              "./cards_simple/5s.jpg": FIVE_SPADES,
              "./cards_simple/5h.jpg": FIVE_HEARTS,
              "./cards_simple/5c.jpg": FIVE_CLUBS,
              "./cards_simple/5d.jpg": FIVE_DIAMONDS,
              "./cards_simple/6s.jpg": SIX_SPADES,
              "./cards_simple/6h.jpg": SIX_HEARTS,
              "./cards_simple/6c.jpg": SIX_CLUBS,
              "./cards_simple/6d.jpg": SIX_DIAMONDS,
              "./cards_simple/7s.jpg": SEVEN_SPADES,
              "./cards_simple/7h.jpg": SEVEN_HEARTS,
              "./cards_simple/7c.jpg": SEVEN_CLUBS,
              "./cards_simple/7d.jpg": SEVEN_DIAMONDS,
              "./cards_simple/8s.jpg": EIGHT_SPADES,
              "./cards_simple/8h.jpg": EIGHT_HEARTS,
              "./cards_simple/8c.jpg": EIGHT_CLUBS,
              "./cards_simple/8d.jpg": EIGHT_DIAMONDS,
              "./cards_simple/9s.jpg": NINE_SPADES,
              "./cards_simple/9h.jpg": NINE_HEARTS,
              "./cards_simple/9c.jpg": NINE_CLUBS,
              "./cards_simple/9d.jpg": NINE_DIAMONDS,
              "./cards_simple/10s.jpg": TEN_SPADES,
              "./cards_simple/10h.jpg": TEN_HEARTS,
              "./cards_simple/10c.jpg": TEN_CLUBS,
              "./cards_simple/10d.jpg": TEN_DIAMONDS,
              "./cards_simple/11s.jpg": QUEEN_SPADES,
              "./cards_simple/11h.jpg": QUEEN_HEARTS,
              "./cards_simple/11c.jpg": QUEEN_CLUBS,
              "./cards_simple/11d.jpg": QUEEN_DIAMONDS,
              "./cards_simple/12s.jpg": JACK_SPADES,
              "./cards_simple/12h.jpg": JACK_HEARTS,
              "./cards_simple/12c.jpg": JACK_CLUBS,
              "./cards_simple/12d.jpg": JACK_DIAMONDS,
              "./cards_simple/13s.jpg": KING_SPADES,
              "./cards_simple/13h.jpg": KING_HEARTS,
              "./cards_simple/13c.jpg": KING_CLUBS,
              "./cards_simple/13d.jpg": KING_DIAMONDS}
