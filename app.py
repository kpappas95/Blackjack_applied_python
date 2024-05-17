import customtkinter as ctk
from deck import deck, Card

WIDTH = 1000
HEIGHT = 600
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        # Calls the constructor of the parent class
        super().__init__()
        # Sets the size of the window
        self.geometry("1000x600")
        # Disables resizing of the window
        self.resizable(width=False, height=False)

        # Creates a frame for the menu with a red foreground color
        self.menuframe = ctk.CTkFrame(self, fg_color="red", width=WIDTH, height=HEIGHT)

        # Creates a button for playing the game
        self.play_button = ctk.CTkButton(self.menuframe, width=100, height=45, text="PLAY")
        # Places the button in the center
        self.play_button.place(x=WIDTH / 2, y=HEIGHT / 2, anchor="center")

        # Creates an option menu for selecting bet values
        self.bet_entry = ctk.CTkOptionMenu(self.menuframe, values=["1", "2", "5", "10", "20"])
        # Places the option menu in the center
        self.bet_entry.place(x=WIDTH / 2, y=200, anchor="center")

        # Creates a label for displaying bet errors
        self.bet_error = ctk.CTkLabel(self.menuframe, text="")

        # Creates the main frame with a green foreground color
        self.mainframe = ctk.CTkFrame(self, fg_color="#04783e")

        # Creates a frame for the deck of cards
        self.deck_frame = ctk.CTkFrame(self.mainframe, fg_color="#04783e")
        # Places the frame in the center
        self.deck_frame.place(x=WIDTH / 2, y=HEIGHT / 2, anchor="center")

        # Creates a frame for the dealer cards
        self.dealer_cards_frame = ctk.CTkFrame(self.mainframe, fg_color="#04783e", width=WIDTH, height=150)
        # Grids the frame in the first row
        self.dealer_cards_frame.grid(row=0, column=0)

        # Creates a frame for the buttons
        self.buttons_frame = ctk.CTkFrame(self.mainframe, fg_color="#04783e", width=WIDTH, height=300)
        # Grids the frame in the second row
        self.buttons_frame.grid(row=1, column=0)

        # Creates a frame for the player cards
        self.player_cards_frame = ctk.CTkFrame(self.mainframe, fg_color="#04783e", width=WIDTH, height=150,
                                               bg_color="blue")
        # Grids the frame in the third row
        self.player_cards_frame.grid(row=2, column=0)

        self.card_images: dict[Card, ctk.CTkLabel] = {}

        # Creates a button for dealing
        self.deal_button = ctk.CTkButton(self.buttons_frame, width=100, height=45, text="DEAL")
        # Places the button at the right
        self.deal_button.place(x=7 * WIDTH / 8, y=HEIGHT / 4, anchor="center")

        # Creates a button for splitting
        self.split_button = ctk.CTkButton(self.buttons_frame, width=100, height=45, text="SPLIT")

        # Creates a button for locking
        self.lock_button = ctk.CTkButton(self.buttons_frame, width=100, height=45, text="LOCK")
        # Places the button at the left
        self.lock_button.place(x=1 * WIDTH / 8, y=HEIGHT / 4, anchor="center")

        # Creates a label for displaying the current score
        self.current_score_label = ctk.CTkLabel(self.mainframe, text="")
        # Places the label in the top-right corner
        self.current_score_label.place(x=90, y=90)

        # Creates a button for displaying the final results
        self.show_results_button = ctk.CTkButton(self.buttons_frame, width=100, height=45, text="SHOW RESULTS")

        # Creates a frame for the game over
        self.game_over_frame = ctk.CTkFrame(self, fg_color="blue", width=WIDTH, height=HEIGHT)
        # Prevents the frame from changing its size based on the size of the widgets inside it
        self.game_over_frame.pack_propagate(False)

        # Creates a label for displaying the game over text
        self.game_over_label = ctk.CTkLabel(self.game_over_frame, text="GAME OVER")
        # Packs the label in the frame
        self.game_over_label.pack(pady=30)

        # Creates a frame for the finale score
        self.score_frame = ctk.CTkFrame(self.game_over_frame, fg_color="#0c5732", width=WIDTH, height=HEIGHT)
        # Creates a label for displaying the score
        self.score_label = ctk.CTkLabel(self.game_over_frame, text="", width=WIDTH)
        # Packs the label in the frame
        self.score_label.pack()

        # Creates a label for displaying whether the player won or lost
        self.result_label = ctk.CTkLabel(self.game_over_frame, text="")
        # Packs the label in the frame
        self.result_label.pack()

        # Creates a button for playing again
        self.play_again_button = ctk.CTkButton(self.game_over_frame, width=100, height=45, text="PLAY AGAIN")
        # Packs the button in the frame
        self.play_again_button.pack(pady=30)

        self.display_menu()

    def display_menu(self):
        # Removes the mainframe and the game_over_frame from the window
        self.mainframe.pack_forget()
        self.game_over_frame.pack_forget()
        self.bet_error.configure(text="")
        # Packs the menuframe in the window
        self.menuframe.pack()

    def display_main_frame(self):
        # Removes the menuframe and the game_over_frame from the window
        self.menuframe.pack_forget()
        self.game_over_frame.pack_forget()
        # Packs the mainframe in the window
        self.mainframe.pack()
        self.display_deck()

    def display_deck(self):
        # For each card in the deck, creates a label, its image being the .image field of the card
        # Places the first card at the center of the window, and each next card slightly higher and to the right
        for index, card in enumerate(deck):
            card_image = ctk.CTkLabel(self.mainframe, text="", image=card.image, width=60, height=101)
            card_image.place(x=(WIDTH // 2) + (0.5 * index), y=(HEIGHT // 2) - (0.2 * index), anchor="center")
            # Fills the card_images dictionary with the key being the card object, and the value being the card label
            self.card_images[card] = card_image
            # Sets the position of each card object as the position of the image in the window
            card.position[0] = int(card_image.place_info()["x"]) - 125  # Tested x offset
            card.position[1] = int(card_image.place_info()["y"]) - 75  # Tested y offset

    def move_card(self, card, position, flip=True, end_of_game=False):
        # Increases or decreases the y position of the card until it reaches the desired y position
        if card.position[1] < position[1]:
            card.position[1] += 1
        elif card.position[1] > position[1]:
            card.position[1] -= 1
        elif card.position[1] == position[1]:
            # If the desired y position is reached, does the same process for the x position
            if card.position[0] < position[0]:
                card.position[0] += 1
            elif card.position[0] > position[0]:
                card.position[0] -= 1

        # Updates the position of the card image
        self.card_images[card].place(x=card.position[0], y=card.position[1], anchor="center")

        # If the card has not reached its final position, move_card is called again with the updated x and y positions of the card
        if not card.position == position:
            self.after(2, lambda: self.move_card(card, position, flip, end_of_game))
        else:
            # If end_of_game is true, displays the "Show Results" button
            if end_of_game:
                self.show_results_button.place(x=WIDTH / 8, y=3 * HEIGHT / 8, anchor="center")
            # If flip is true, flips the card and updates its image
            if flip:
                card.flip()
            self.card_images[card].configure(image=card.image)

    def delete_card_labels(self):
        # Removes the values of each key in the card_images dictionary
        for card in self.card_images.keys():
            self.card_images[card].destroy()

    def display_game_over(self):
        # Removes the mainframe from the window
        self.mainframe.pack_forget()
        # Packs the game_over_frame in the window
        self.game_over_frame.pack(expand=True)
