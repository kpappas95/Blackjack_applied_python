import random
import customtkinter as ctk
from PIL import Image

suits = ["clubs", "diamonds", "hearts", "spades"]
faces = ["jack", "queen", "king", "ace"]


class Card:
    def __init__(self, value, suit, point):
        self.value = value
        self.suit = suit
        # Image path is either a path to the face-up or face-down card
        self.image_path = ["assets/images/" + str(self.value) + "_of_" + self.suit + ".png", "assets/images/upside_down.jpg"]
        self.point = point
        self.image = ctk.CTkImage(light_image=Image.open(self.image_path[1]), size=(60, 101))
        self.position = [0, 0]

    # Sets how each card object will be represented
    def __repr__(self):
        return str(self.value) + " of " + self.suit  # Example: 3_of_hearts

    # Changes the image from the face-down to face-up
    def flip(self):
        self.image = ctk.CTkImage(light_image=Image.open(self.image_path[0]), size=(60, 101))


class Deck(list):
    def __init__(self):
        super().__init__()
        self.generate_cards()

    def shuffle(self):
        random.shuffle(self)

    def generate_cards(self):
        # We generate every 2, 3, 4 ... J, Q, K and A
        for i in range(2, 15):
            # Cards from 2-10 will have a value same as the card number
            if i <= 10:
                value = i
            # Else the value will either be "jack", "queen", "king" or "ace"
            else:
                value = faces[i - 11]
            # Aces will initially count as 1
            if i == 14:
                point = 1
            # Cards from 10 and above will count as 10
            elif i >= 10:
                point = 10
            # The rest of the cards will count as the number of the card
            else:
                point = i
            # We generate all 3 suits for each value
            for suit in suits:
                # We create a Card object with those 3 parameters, and we append this Card to the Deck(list)
                card = Card(value, suit, point)
                self.append(card)


deck = Deck()
