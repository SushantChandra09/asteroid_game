#For tests only
from Game import *
from sys import argv as cmd
cmd.pop(0)
# Logic for cleaning the leaderboard from system argv and starting the game.
if not len(cmd):
    print("Tip: to clean all records, type 'python3 main.py clear_records'")
    Game()
if cmd[-1] == "clear_records":
    password = input("Password: ")
    if password == game["password"]:
        ans = input("\033[93mALERT: This will erase all the stored data. Do you want to continue? [y/n]\033[0m")
        if ans == "y":
            print("\033[92mOperation succeded.\033[0m\nStarting the game...")
            with open("records.csv", 'w') as data:
                data.write("1,,0\n2,,0\n3,,0\n4,,0\n5,,0")
            Game()
        elif ans == "n":
            print("Operation aborted. Starting the game.")
            Game()
        else:
            print("Not recognized command. Please, try again.")
    else:
        print("Wrong password. Operation aborted.\nStarting the game.")
        Game()
else:
    print("Error: Not recognized command.\nOperation Canceled.\nInitializing the game.")
    Game()
