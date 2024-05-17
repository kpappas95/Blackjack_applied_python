WIDTH = 1000


class Player:
    def __init__(self, name="Mad Clip"):
        self.name = name
        self.tokens = 0
        self.bet = 0
        self.cards = [[], []]
        self.card_positions = {}
        self.split_card_positions = {}
        self.total = 0
        self.split_total = 0
        self.locked = False
        self.lost = False
        self.split_lost = False
        self.did_split = False
        self.current_hand = 0
        self.can_split = False

    # This method will be called each time the player receives a card
    # It creates the positions depending on how many cards the player has, and it makes sure that all positions are centered
    def generate_card_positions(self):
        # For the original hand.
        for index in range(len(self.cards[0])):
            self.card_positions[index] = [WIDTH / 2 + index * 80 - 40 * (len(self.cards[0]) - 1), 420]
        # For the split hand - if the player splits
        for index in range(len(self.cards[1])):
            self.split_card_positions[index] = [WIDTH / 2 + index * 80 - 40 * (len(self.cards[1]) - 1), 530]

    def lock(self):
        self.locked = True

    def calculate(self):
        # Checks if the player has an ace
        player_has_ace = False
        self.total = 0
        for card in self.cards[self.current_hand]:
            self.total += card.point
            if card.value == "ace":
                player_has_ace = True
        # If they have, we add 10 to the player's total to make the ace count for 11 points instead of 1
        if player_has_ace:
            self.total += 10
            # If the total exceeds 21, we make the ace count for the original 1 point
            if self.total > 21:
                self.total -= 10

    def check_for_split(self):
        if self.current_hand == 0:
            # If the first two cards have the same value, the player can split
            self.can_split = self.cards[0][0].point == self.cards[0][1].point

    def split(self):
        self.did_split = True
        self.current_hand = 1
        # We put the last card of the original hand in the split hand
        self.cards[1].append(self.cards[0].pop())
        self.can_split = False

    def reset(self):
        self.cards = [[], []]
        self.card_positions.clear()
        self.total = 0
        self.split_total = 0
        self.locked = False
        self.lost = False
        self.did_split = False
        self.current_hand = 0
        self.can_split = False


class Dealer:
    def __init__(self):
        self.cards = []
        self.card_positions = {}
        self.total = 0
        self.locked = False
        self.lost = False

    def generate_card_positions(self):
        for index in range(len(self.cards)):
            self.card_positions[index] = [WIDTH / 2 + index * 80 - 40 * (len(self.cards) - 1), 110]

    def lock(self):
        self.locked = True

    def calculate(self):
        player_has_ace = False
        self.total = 0
        for card in self.cards:
            self.total += card.point
            if card.value == "ace":
                player_has_ace = True
        if player_has_ace:
            self.total += 10
            if self.total > 21:
                self.total -= 10
        # Prevents the dealer from taking another card if the total already exceeds 17
        if self.total >= 17:
            self.lock()

    def reset(self):
        self.cards = []
        self.card_positions.clear()
        self.total = 0
        self.locked = False
        self.lost = False


# Creates the player and the dealer
player = Player()
dealer = Dealer()