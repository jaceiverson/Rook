# standard library stuff
import random
import json
import socket
import datetime as dt

# pypy stuff
import pandas as pd

# pygame stuff
from pygame import mixer
from tkinter import Tk, LabelFrame, Button, W, E
from PIL import Image, ImageTk

# import some local classes too
from game_play import Player, Trick, Card, get_players, make_deck_list, shuffle_deck


def distribute_cards(cards: list[Card], players: list[Player]):
    # after cards are suffled give them to the players
    player_names = list(players.keys())
    players_order = [player_names[0], player_names[2], player_names[1], player_names[3]]
    return {
        players_order[x]: Player(
            players_order[x],
            x + 1,
            cards[x],
            players[players_order[x]]["Team"],
        )
        for x in range(len(players_order))
    }


def deal(shuffled_deck):
    # check for re-deal (no pointers in your hand)
    player1 = shuffled_deck[:13]
    player2 = shuffled_deck[13:26]
    player3 = shuffled_deck[26:39]
    player4 = shuffled_deck[39:52]
    widow = shuffled_deck[52:]

    dealt_cards = [player1, player2, player3, player4, widow]
    for x in dealt_cards[:4]:
        # checks to make sure you have at least one pointer in your hand
        if sum(y.pvalue for y in x) == 0:
            # to be honest, I think this works, but I am not sure. Hopefully we don't ever run into it.
            new_shuffle = random.shuffle(shuffled_deck)
            return deal(new_shuffle)

    # order them by suit, and then by tValue
    for y in range(len(dealt_cards)):
        dealt_cards[y].sort(key=lambda y: [y.suit, y.tvalue], reverse=True)

    return dealt_cards


def validate_bid(player, min_bid, pass_count):
    # check to make sure the input is valid
    good_input = False
    while not good_input:
        bid = input("BID: ")
        try:
            int_bid = int(bid)
            if int_bid >= min_bid and int_bid <= 180:
                good_input = True
            else:
                print("Enter a valid number", min_bid, " - ", "180")
        except ValueError as e:
            if bid.lower() == "pass":
                int_bid = 0
                good_input = True
            else:
                print("Enter a valid number", min_bid, " - ", "180")
    player.set_bid(int_bid)

    if player.bid == 0:
        min_bid = min_bid
        pass_count += 1
    elif player.bid >= min_bid:
        min_bid = int_bid + 5

    return int_bid, min_bid, pass_count


def show_widow(widow, player):
    print(f"Widow. Taken at {str(player.bid)} by " + player.name)
    for x in widow:
        print(x.suit, x.number)


def bid_sequence(players):
    winner = False
    max_bidder = ""
    max_bid = 0
    pass_count = 0
    current_bid = 0
    bid_leader = ""
    min_bid = 100
    while not winner:
        for x in players:
            if x.bid > 0:
                if pass_count > 2:
                    max_bidder = x
                    max_bidder.hand = x.hand
                    winner = True
                    break
                print(x.name + "'s bid")
                print("Type your bid. You must bid at least: " + " " + str(min_bid))
                current_bid, min_bid, pass_count = validate_bid(x, min_bid, pass_count)
                if current_bid > 0:
                    print(f"Current bid  is @ {str(current_bid)}")

    print(max_bidder.name + " has won the bid at " + str(max_bidder.bid) + ".")

    good_input = False
    while not good_input:
        try:
            up_bid = input(
                f"If you would like to increase your bid, please put a value greater than {str(max_bidder.bid)}"
            )
            if int(up_bid) % 5 != 0:
                print("Bid must be a multiple of 5. Try again.")
            else:
                good_input = True
        except ValueError as e:
            if up_bid.lower() in ["no", "pass"]:
                up_bid = max_bidder.bid
                good_input = True
            up_bid = 0

    if int(up_bid) > max_bidder.bid:
        max_bidder.set_bid(up_bid)

    return max_bidder


def pregame_details(player):
    """
    :param player: player who won the widow and now needs to drop cards
    :return: which cards were dropped as well as what suit is trump
    """
    print("Which cards would you like to drop?")
    dropped_cards_list = []
    while len(dropped_cards_list) < 5:
        player.show_hand()
        good_input = False
        while not good_input:
            try:
                drop = int(input("Index number to drop: "))
                good_input = True
            except ValueError as e:
                print("Please put in a valid input")
        dropped_card = player.drop_card(drop)
        dropped_cards_list.append(dropped_card)

    print("Final Hand:")
    player.show_hand()
    suits = ["Black", "Green", "Yellow", "Red"]
    print("Which suit is going to be trump?")
    print(suits)

    good_input = False
    while not good_input:
        trump_input = input("")

        if trump_input.title() in suits:
            trump = trump_input.title()
            good_input = True
        else:
            print("Please use a valid input")

    return dropped_cards_list, trump


def assign_trump_to_cards(trump_suit, players):
    """
    :param trump_suit: suit previously declared as trump
    :param players: list of players
    :return: nothing, assigns all the cards in player's hands to trump
    """
    for x in players:
        for y in x.hand:
            # also assign each card to its owner
            y.owner = x
            if y.suit in [trump_suit, "Rook"]:
                y.trump = True


def create_trick(num):
    """
    :param num: number of the trick (number is order sequencial of trick
    :return: trick object
    """
    return Trick(num)


def play_tricks(players, starting_player, play_order):
    num_tricks = 13
    trick_winner = starting_player

    tricks = []

    for x in range(num_tricks):
        # create a new trick and add it to the list
        current_trick = create_trick(x + 1)
        tricks.append(current_trick)
        # change the trick order
        section_a = play_order[play_order.index(trick_winner.name) :]
        section_b = play_order[: play_order.index(trick_winner.name)]
        play_order = section_a + section_b
        for trick_player_order, y in enumerate(play_order, start=1):
            current_player = players[y]
            player_card = play_hand(current_player, current_trick, trick_player_order)
            # assign the card to the order in the trick
            if trick_player_order == 1:
                current_trick.first_card = player_card
            elif trick_player_order == 2:
                current_trick.second_card = player_card
            elif trick_player_order == 3:
                current_trick.third_card = player_card
            elif trick_player_order == 4:
                current_trick.forth_card = player_card

            print(
                current_player.name
                + " plays "
                + player_card.suit
                + " "
                + str(player_card.number)
            )

        trick_winner = current_trick.winning_pair()
        current_trick.find_points()
        current_trick.print_trick()

    return tricks


def play_hand(player, trick, count):
    """
    :param player:
    :param trick:
    :param count:
    :return:

    TODO - Server needs to
    1) SEND show_hand (tkinter/socket)
    2) RECEIVE card_to_play (from network device)
    3) BROADCAST the card that was played
    """
    try:
        lead_suit = trick.first_card.suit
        lead_is_trump = trick.first_card.trump
    except:
        lead_suit = None
        lead_is_trump = False
    # shows entire hand
    player.show_hand()

    # shows what cards, if available
    available_cards = player.available_cards(lead_suit, count, lead_is_trump)

    good_input = False
    while not good_input:
        try:
            card = int(input("Index of card to play: "))
            if card <= len(available_cards):
                good_input = True
            else:
                print("Not an availible card")
                available_cards = player.availible_cards(lead_suit, count)
        except ValueError as e:
            print("Please put in a valid input")
    card_to_play = available_cards[card - 1]

    # removes the card from the players hand
    # don't worry it is added to the trick object for later
    player.hand.remove(card_to_play)

    return card_to_play


def find_winner(all_tricks, widow, bid_winner):
    team_1 = 0
    team_2 = 0
    final_trick_winning_team = all_tricks[12].winning_player.team
    bidding_team = bid_winner.team
    game_resolution = ""

    for x in all_tricks:
        if x.winning_player.team == 1:
            team_1 += x.point_value
        else:
            team_2 += x.point_value

    widow_points = 0
    for x in widow:
        print(x.suit, x.number)
        widow_points += x.pvalue
    print("Widow Point value: ", widow_points)

    if final_trick_winning_team == 1:
        team_1 += widow_points
    else:
        team_2 += widow_points

    if bidding_team == 1:
        if bid_winner.bid > team_1:
            team_1 = bid_winner.bid * -1
            game_resolution = "Team 1 didn't reach their bid"
        else:
            team_1 = bid_winner.bid
            game_resolution = "Team 1 reached their bid"
    elif bid_winner.bid > team_2:
        team_2 = bid_winner.bid * -1
        game_resolution = "Team 2 didn't reach their bid"
    else:
        team_2 = bid_winner.bid
        game_resolution = "Team 2 reached their bid"

    # final check for a grandslam
    if team_1 == 180:
        team_1 = 180
        game_resolution = "Team 1 Grand Slam"
    elif team_2 == 180:
        team_2 = 180
        game_resolution = "Team 2 Grand Slam"

    return print_results(team_1, team_2, game_resolution)


def print_results(one, two, resolution):
    print(resolution)
    print(f"Team 1 Score: {str(one)}")
    print(f"Team 2 Score: {str(two)}")
    return {"Team 1 Score": one, "Team 2 Score": two, "Outcome": resolution}


def play_one_hand_of_rook(playerList: str):
    # make the cards and shuffle them
    cards = make_deck_list()
    shuffled_deck = shuffle_deck(cards)

    # deal cards: returns list of lists. Order -> 1,2,3,4, widow
    dealt_cards = deal(shuffled_deck)
    widow = dealt_cards[4]

    # get the list of players class and list of player names
    players = distribute_cards(dealt_cards, playerList)

    # bidding sequence
    bid_winner = bid_sequence(list(players.values()))
    show_widow(widow, bid_winner)
    bid_winner.hand += widow
    end_widow, trump = pregame_details(bid_winner)
    assign_trump_to_cards(trump, list(players.values()))

    # sendHandstoPlayers

    # play the game return a list of tricks
    tricks = play_tricks(players, bid_winner, list(players.keys()))

    # calculate and print results
    results = find_winner(tricks, end_widow, bid_winner)

    return tricks, results


def play_rook():
    team1 = 0
    team2 = 0
    players = get_players()
    date = dt.datetime.now().strftime("%Y-%m-%d %r")
    while team1 < 500 and team2 < 500:
        game_count = 1
        tricks, game_results = play_one_hand_of_rook(players)
        master_game_scorecard = {f"Game {game_count}": game_results}
        team1 += game_results["Team 1 Score"]
        team2 += game_results["Team 2 Score"]

        df = pd.DataFrame([vars(f) for f in tricks])

        df.to_csv(
            "/game_data/game_" + date + ".xlsx",
        )

        game_count += 1


# TODO
"""

Work on making Tkinter GUI for the game
send the info out to the local network
none of these functions are working
show hand will display the cards, but not allow you to click to send them anywhere

I have taken a break from this, but want to get it to work

Sockets was working, I can send data over the local network, but I am having a hard time sending it back and forth
"""


def show_hand(hand):
    mixer.init()
    root = Tk()
    root.title("Hand")
    root.resizable(False, False)

    # Frame for the buttons.
    btn_frame = LabelFrame(root)
    btn_frame.grid(row=0, column=1)

    # Frame for the two card images.
    cards_frame = LabelFrame(root, pady=4)
    cards_frame.grid(row=1, column=0, padx=10, pady=5)

    # Frame for the change button.
    chng_btn_frame = LabelFrame(root)
    chng_btn_frame.grid(row=1, column=0, sticky=W, padx=10, pady=10)

    # Frame for printing the scores.
    score_frame = LabelFrame(root)
    score_frame.grid(row=2, column=0, padx=10, columnspan=2, sticky=W + E)

    # Frame for printing messages.
    msg_frame = LabelFrame(root)
    msg_frame.grid(row=3, column=0, padx=10, columnspan=2, sticky=W + E)

    cards = []
    images = []

    for card, idx in enumerate(hand):
        cards.append(Button(cards_frame, command=show_back))
        images.append(
            Image.open("./rook/resources/card-img/" + card.short_name() + ".jpg")
        )
        PHOTO = ImageTk.PhotoImage(images[idx].resize((75, 120), Image.BOX))

        cards[idx].config(image=PHOTO)

        cards[idx].grid(row=1, column=idx + 1, padx=2, pady=2)

        cards[idx].photo = PHOTO

    root.mainloop()


def show_back():
    back = Image.open("./rook/resources/card-img/back.jpg")
    PHOTO = ImageTk.PhotoImage(back.resize((75, 120), Image.BOX))
    back.config(image=PHOTO)
    back.grid(row=1, column=1, padx=2, pady=2)
    back.photo = PHOTO


def set_up_socket(hand, x):
    """
    socket test?

    for x in range(len(dealt_cards)):
        if len(dealt_cards[x])>5:

            data=pickle.dumps(dealt_cards[x])
            sock=setUpSocket(data,x)
        else:
            #this is the widow and doesn't need to be sent out yet.
            pass
    """

    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    port = int(6001 + x)
    print(host, port)
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    print(f"Connection accepted from {repr(addr[1])}")
    c.send(hand)
    c.close()

    return s


# idk?
def show_hand_test():
    # make the cards and shuffle them
    cards = make_deck_list()
    shuffled_deck = generate_shuffled_deck(cards)

    # deal cards: returns list of lists. Order -> 1,2,3,4, widow
    dealt_cards = deal(shuffled_deck)
    widow = dealt_cards[4]

    for x in dealt_cards:
        show_hand(x)


if __name__ == "__main__":
    play_rook()
