import random
import threading
import pygame
from player import *
import deck
from app import *
from db_handler import *

# Checks when the program last run
check_last_run()

WIDTH = 1000
HEIGHT = 600

# Strings that will be later used in fstrings to load .wav files
win_sounds = ["goddamn", "next_time"]
lose_sounds = ["beat_me", "haha", "nice_try"]


def start_game():
    # Sets the player tokens
    set_player_tokens()
    # Gets the player's bet
    bet = int(app.bet_entry.get())
    app.bet_error.place(x=WIDTH / 2, y=400, anchor="center")
    # Displays the error message (if the tokens are not enough for the selected bet)
    if bet > player.tokens:
        app.bet_error.configure(text="YOU DON'T HAVE ENOUGH TOKENS")
    else:
        player.bet = bet
        # Removes the bet value from the player tokens
        set_player_tokens(player.bet * -1)
        # Shuffles the deck
        deck.shuffle()
        # Displays the main frame
        app.display_main_frame()
        # Removes any buttons from previous rounds
        app.split_button.place_forget()
        app.show_results_button.place_forget()
        check_for_empty_deck()
        # Deals one card to the player and one to the dealer
        deal_initial_cards()
        check_for_empty_deck()
        deal_initial_cards()
        # Calculates the player total
        player.calculate()
        # Checks if the player can split
        player.check_for_split()
        if player.can_split:
            # Displays the split button
            app.split_button.place(x=7 * WIDTH / 8, y=3 * HEIGHT / 8, anchor="center")
            app.split_button.configure(command=split)
        # Updates the current total and the remaining tokens of the player
        app.current_score_label.configure(text=f"""CURRENT TOTAL: {player.total}
    
    TOKENS LEFT: {player.tokens}""")
        app.lock_button.configure(state="normal")
        app.deal_button.configure(state="normal")


# Plays a .wav file
# If the loops is -1, the file loops over and over until the program terminates
def play_wav_file(file_path, loops=0):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play(loops=loops)


# Moves the player cards into position
def move_player_cards():
    player.generate_card_positions()
    for index, card in enumerate(player.cards[0]):
        app.move_card(card, player.card_positions[index])
    for index, card in enumerate(player.cards[1]):
        app.move_card(card, player.split_card_positions[index])


def deal_card():
    # Temporarily disables the deal button
    app.deal_button.configure(state="disabled")
    app.split_button.place_forget()
    check_for_empty_deck()
    # Removes a card from the deck and puts it in the current hand of the player
    player.cards[player.current_hand].append(deck.pop())
    move_player_cards()
    player.calculate()
    app.current_score_label.configure(text=f"""CURRENT TOTAL: {player.total}

        TOKENS LEFT: {player.tokens}""")
    # Re-enables the deal button if the current total is less than 21 or if the player just lost in the split hand
    if player.total <= 21 or player.split_lost:
        app.deal_button.configure(state="normal")
        # Checks the result
        check_result(locked=False)
    else:
        if not player.did_split:
            # The total exceeds 21 and the player has not split, so the dealer wins
            app.deal_button.configure(state="disabled")
            app.lock_button.configure(state="disabled")
            # Checks the result after 1.5s
            app.after(1500, lambda: check_result(True))
        else:
            lock()
            app.deal_button.configure(state="normal")
            check_result(False)


def split():
    player.split()
    app.split_button.place_forget()
    move_player_cards()


# Checks if the deck is empty and regenerates the cards
def check_for_empty_deck():
    if not deck:
        deck.generate_cards()
        deck.shuffle()
        app.display_deck()


def deal_initial_cards():
    check_for_empty_deck()
    # Removes a card from the deck and puts it in the player's original hand
    player.cards[0].append(deck.pop())
    move_player_cards()
    check_for_empty_deck()
    # Removes a card from the deck and puts it in the dealer's hand
    dealer.cards.append(deck.pop())
    dealer.generate_card_positions()
    # Moves the dealer's cards but doesn't flip them
    for index, card in enumerate(dealer.cards):
        if index == 0:
            app.move_card(card, dealer.card_positions[index])
        else:
            app.move_card(card, dealer.card_positions[index], flip=False)
    dealer.calculate()


# Displays the menu and resets the player and dealer stats
def reset_game():
    app.display_menu()
    player.reset()
    dealer.reset()
    clear_cards()


def clear_cards():
    app.delete_card_labels()


def lock():
    # If the player locks on the original hand the dealer takes cards
    if player.current_hand == 0:
        app.lock_button.configure(state="disabled")
        app.deal_button.configure(state="disabled")
        deal_to_dealer()
    # If the player locks on the split hand we keep the split total and the player moves on with the original hand
    else:
        player.split_total = player.total
        print(player.split_total)
        player.current_hand = 0
    player.calculate()


def deal_to_dealer():
    while len(deck) >= 1 and not dealer.locked:
        # removes a card from the deck and puts it in the dealer's hand
        dealer.cards.append(deck.pop())
        dealer.calculate()
    dealer.generate_card_positions()
    # Moves the dealer cards into position
    for index, card in enumerate(dealer.cards):
        if index == len(dealer.cards) - 1:
            app.move_card(card, dealer.card_positions[index], end_of_game=True)  # end_of_game is used to display the results button
        else:
            app.move_card(card, dealer.card_positions[index])


def check_result(locked=False):
    sound = None
    result_label_text = ""
    # The best hand of the player will be used for comparison
    if 21 >= player.split_total > player.total:
        player.total = player.split_total
    app.score_label.configure(text=f"YOUR SCORE: {player.total}       DEALER'S SCORE: {dealer.total}")
    # For comparisons when the player is not locked on both hands
    if not locked:
        if player.total > 21:
            # If the player has not split the dealer wins
            if not player.did_split:
                player.lost = True
                result_label_text = "YOU LOST!"
                # Chooses a random sound from the lose_sounds list
                sound = random.choice(lose_sounds)
                time.sleep(0.5)
                app.display_game_over()
            # Otherwise we keep the split hand if it is better than the original hand
            else:
                if player.split_total <= 21:
                    player.total = player.split_total
    else:
        # Checks different results and sets the message, sound and player tokens accordingly
        if player.total == 21:
            result_label_text = "BLACKJACK! YOU WON!"
            # Chooses a random sound from the win_sounds list
            sound = random.choice(win_sounds)
            set_player_tokens(player.bet * 2)
        elif dealer.total == 21:
            result_label_text = "BLACKJACK! YOU LOST!"
            sound = random.choice(lose_sounds)
        elif player.total > 21:
            player.lost = True
            result_label_text = "YOU LOST!"
            sound = random.choice(lose_sounds)
        elif dealer.total > 21:
            dealer.lost = True
            result_label_text = "YOU WON!"
            sound = random.choice(win_sounds)
            set_player_tokens(player.bet * 2)
        elif player.total > dealer.total:
            result_label_text = "YOU WON!"
            sound = random.choice(win_sounds)
            set_player_tokens(player.bet * 2)
        else:
            result_label_text = "YOU LOST!"
            sound = random.choice(lose_sounds)
        time.sleep(0.5)
        # Displays the game over screen
        app.display_game_over()
    if sound:
        # Creates a thread for the dealer's sounds
        sound_thread = threading.Thread(target=play_wav_file, args=(f"assets/audio/{sound}.wav", ), daemon=True)
        sound_thread.start()
    app.result_label.configure(text=f"{result_label_text}")


# Creates the window
app = App()
# Creates a thread for the background music
bg_music_thread = threading.Thread(target=play_wav_file, args=(f"assets/audio/background_music.mp3", -1), daemon=True)
bg_music_thread.start()
# Button configurations
app.play_button.configure(command=start_game)
app.lock_button.configure(command=lock)
app.deal_button.configure(command=deal_card)
app.show_results_button.configure(command=lambda: check_result(True))
app.play_again_button.configure(command=reset_game)

app.mainloop()