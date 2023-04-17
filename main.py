import apikey
import requests
import random
import webbrowser

url = 'https://api.ausmash.com.au'
auth = {"X-ApiKey": apikey.key}

print("Welcome to Barney's guess the elo! Please wait while I fetch some vods.")

api_players = requests.get(url + "/players", headers = auth).json()

temp_player_list = []

for i in api_players:
    temp_player_list.append(i)

vod_count = 0
rand_player = {}

while(vod_count == 0):

    rand_player = temp_player_list[random.randint(1, len(temp_player_list)) - 1]

    api_vods = requests.get(rand_player["APILink"] + "/videos", headers = auth).json()

    vod_count = len(api_vods)

player_elo = requests.get(rand_player["APILink"] + "/elo", headers = auth).json()

rand_vod = api_vods[random.randint(1, len(api_vods)) - 1]

game = rand_vod["Match"]["Event"]["Game"]

print("\nToday you're gonna guess", rand_player["Name"] + "'s elo in", game["Name"])

game_elo = 0

for i in player_elo:
    if i["Game"]["ID"] == game["ID"]:
        game_elo = i["Elo"]

webbrowser.open(rand_vod["Url"])

attempts_left = 5

tab = "    "

while attempts_left > 0:

    print("\n" + tab, attempts_left, "Attempts left")
    elo_guess = int(input(tab + " " + "Enter your guess: "))

    if elo_guess == game_elo:
        print(tab, "That's correct! Good job!")
        attempts_left = 0
    else:
        diff = abs(elo_guess - game_elo)
        if diff < 10:
            print(tab, "Less than 10 off! You're so close!")
        elif diff < 30:
            print(tab, "Less than 30 off! You've nearly got it!")
        elif diff < 50:
            print(tab, "Getting hot! You're less than 50 off.")
        elif diff < 100:
            print(tab, "Fairly close! You're less than 100 off.")
        elif diff < 200:
            print(tab, "Close! You're less than 200 off.")
        elif diff < 500:
            print(tab, "You're off by less than 500.")
        elif diff < 1000:
            print(tab, "Try again, you're off by less than 1000.")
        else:
            print(tab, "Not even close. You're way off.")
        
        if elo_guess - game_elo > 0:
            print(tab, "It's lower.")
        else:
            print(tab, "It's higher.")

        attempts_left -= 1
        if attempts_left == 0:
            print(tab, rand_player["Name"] + "'s elo was", game_elo)

input("\nThanks for playing guess the ausmash elo!")