import random as r


def numPlayers(pre_set):
    numPlay = int(input("How many players?")) if pre_set == 0 else pre_set
    players = []
    for x in range(numPlay):
        tempPlayer = input(f"Player {str(x + 1)} name: ")
        players.append(tempPlayer)
    return players


def initTeams(numPlay, counter, pre_set_team):
    # randomize team
    if pre_set_team == 0:
        if counter == 0:
            print(f"You have {str(numPlay)}" + " players.\n")
            numTeams = int(input("How many teams? "))
        else:
            numTeams = counter
    else:
        numTeams = pre_set_team

    return [[] for _ in range(numTeams)]


def setTeams(t, players):
    sizeRand = len(players)
    usedPlayers = []

    while len(players) > 0:
        for x in range(len(t)):
            selection = r.randrange(0, sizeRand)
            # ensures the selection will be a non previously selected player
            while players[selection] in usedPlayers:
                selection = r.randrange(0, sizeRand)

            t[x].append(players[selection])

            usedPlayers.append(players[selection])
            players.remove(players[selection])

            if len(players) < 1:
                break
            else:
                sizeRand -= 1
    return t, usedPlayers


def printTeams(team_print):
    for x in team_print:
        print(f"Team {str(team_print.index(x) + 1)}: {str(x)}")


def main(num_players=0, teams=0):
    players = numPlayers(num_players)
    repeat = 0
    while True:
        team_blank = initTeams(len(players), repeat, teams)
        finalTeamSet, players = setTeams(team_blank, players)
        printTeams(finalTeamSet)

        redo = input("\nReshuffle teams? (Enter)\nIf you want to exit type something")
        if redo != "":
            break
        else:
            repeat = len(team_blank)

    return finalTeamSet[0] + finalTeamSet[1]


def randomize_teams():
    players = main(4, 2)
    return [players[0], players[2], players[1], players[3]]


def get_players() -> list[str]:
    good_input = False
    while not good_input:
        gen_teams = input("Generate random teams? (y/n)")
        if gen_teams.lower() in ("y", "n"):
            good_input = True
        else:
            print("Valid input please")
    players = {}

    if gen_teams.lower() == "y":
        players_order = randomize_teams()
        players[players_order[0]] = {"Team": 1}
        players[players_order[2]] = {"Team": 1}
        players[players_order[1]] = {"Team": 2}
        players[players_order[3]] = {"Team": 2}
    else:
        for x in range(4):
            if x == 0:
                print("Team 1")
            elif x == 2:
                print("Team 2")
            temp = input(f"Player {str(x + 1)} name: ")
            team = 1
            if x >= 2:
                team = 2
            players[temp] = {"Team": team}

    return players
