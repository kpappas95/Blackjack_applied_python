import os
import time
import csv
from player import player


def read_last_run_time():
    if os.path.exists("last_run.txt"):
        with open("last_run.txt", "r") as file:
            last_run_time = file.read()
            return float(last_run_time)
    else:
        return 0


def write_last_run_time():
    current_time = time.time()
    with open("last_run.txt", "w") as file:
        file.write(str(current_time))


def check_last_run():
    # Gets the time of the last run
    last_run_time = read_last_run_time()
    current_time = time.time()

    if current_time - last_run_time >= 24 * 60 * 60:  # Check if it's been more than 24 hours
        # Checks if the file exists
        if os.path.exists("fake_db.csv"):
            with open("fake_db.csv", "r+") as f:
                c = csv.reader(f)
                for row in c:
                    # Sets the player tokens to be 20 more than what the last item in the line is
                    player.tokens = int(row[-1]) + 20
                f.seek(0)
                # Updates the line to show the new token value
                f.write(f"TOKENS,{player.tokens}")
                f.truncate()
        # Writes the last time the program run in a file
        write_last_run_time()
    set_player_tokens()


def set_player_tokens(amount=0):
    if not os.path.exists("fake_db.csv"):
        # The first time this program runs, the player tokens will be set to 100
        player.tokens = 100
        with open("fake_db.csv", "w") as f:
            f.write("TOKENS,100")
    else:
        with open("fake_db.csv", "r") as f:
            c = csv.reader(f)
            for row in c:
                # Sets the tokens based on the result of the game
                player.tokens = int(row[-1]) + amount
        with open("fake_db.csv", "w") as f:
            f.write(f"TOKENS,{player.tokens}")
