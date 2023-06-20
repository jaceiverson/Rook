import pickle
import random


class Player:
    def __init__(
        self,
        name: str,
        num: int,
        hand: list = None,
        team: int = None,
        bid: int = 100,
        location: str = None,
        socket_obj=None,
    ):
        # entered name
        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError("Name must be a string")
        # player seat number
        if num in range(4):
            self.num = num
        else:
            raise ValueError("Player number must be between 1 and 4")

        # what their max bid was, defaults to 100
        self.bid = bid
        # what team (1/2) the player is on
        self.team = team
        # need to save the location (internet) of player to send things via socket
        self.location = location
        # save the entire socket object of the person
        self.socket_obj = socket_obj

    def set_hand(self, hand: list) -> None:
        # player hand list of card objects
        if isinstance(hand, list) and len(hand) == 13 and isinstance(hand[0], Card):
            self.hand = hand
        else:
            raise ValueError("Hand must be a list of 13 card objects")

    def show_hand(self):
        # print the list of hands to the console
        self.hand.sort(key=lambda x: [x.suit, x.tvalue], reverse=True)
        print(f"{self.name}'s Hand")
        for x in range(len(self.hand)):
            print(x + 1, self.hand[x].suit, self.hand[x].number)

    def available_cards(self, lead_suit: str, count: int, lead_suit_is_trump: bool):
        # determines which cards are available to play each trick
        print("Available Cards to Play")
        available = []
        if count == 1:
            # if this is the first card played this trick
            available = self.hand
            for y in range(len(available)):
                print(
                    str(y + 1)
                    + " "
                    + available[y].suit
                    + " "
                    + str(available[y].number)
                )
        else:
            for x in range(len(self.hand)):
                if self.hand[x].suit == lead_suit or (
                    self.hand[x].number == 20 and lead_suit_is_trump
                ):
                    available.append(self.hand[x])
            if len(available) == 0:
                for x in range(len(self.hand)):
                    if self.hand[x].trump:
                        available.append(self.hand[x])

            if len(available) == 0:
                print("You can play anything, but it is a non-factor to the trick")
                available = self.hand
            else:
                print("You must play one of the following cards")
                for y in range(len(available)):
                    print(
                        str(y + 1)
                        + " "
                        + available[y].suit
                        + " "
                        + str(available[y].number)
                    )

        return available

    def drop_card(self, card):
        dropped_card = self.hand[card - 1]
        self.hand.remove(self.hand[card - 1])
        return dropped_card

    def set_bid(self, bid):
        self.bid = bid

    def set_hand(self, hand):
        self.hand = hand

    def close_socket(self):
        self.socket_obj.close()

    def update_hand_client_side(self):
        new_hand = self.socket_obj.recv(4096)
        self.set_hand(new_hand)

    def update_hand_server_side(self):
        self.socket_obj.send(pickle.dumps(self.hand))

    def update_hand_network(self):
        self.update_hand_server_side()
        self.update_hand_client_side()

    def __repr__(self):
        return f"Player: {self.name}"

    def __str__(self):
        return f"Player: {self.name}"


class Team:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.game_score = 0

    def __repr__(self):
        return f"Team: {self.player1.name} and {self.player2.name}"

    def __str__(self):
        return f"Team: {self.player1.name} and {self.player2.name}"


class Card:
    def __init__(
        self,
        suit: str,
        number: int,
        pvalue: int,
        tvalue: int,
        trump: bool = False,
    ):
        # suit of the card object
        if suit.lower() in {"red", "green", "yellow", "black", "rook"}:
            self.suit = suit.lower()
        else:
            raise ValueError("Suit must be red, green, yellow, or black")

        # number on the card
        if number in range(1, 15) or number == 20:
            self.number = number
        else:
            raise ValueError("Number must be between 1 and 14 or 20")

        # Point Value of the card
        if pvalue in {0, 5, 10, 15, 20}:
            self.pvalue = pvalue
        else:
            raise ValueError("Point value must be 0, 5, 10, 15, or 20")

        # Trick Value of card
        if tvalue in range(2, 16) or tvalue == 20:
            self.tvalue = tvalue
        else:
            raise ValueError("Trick value must be between 2 and 15 or 20")

        # BOOLEAN if the card is trump
        if trump in {True, False}:
            self.trump = trump
        else:
            raise ValueError("Trump must be a boolean object: True or False")

        # each card pertains to a particular player
        self.owner = None

    def short_name(self):
        # card short name is the first letter of the suit and the number
        # unless the card is a rook, then it is rk
        return self.suit[0].lower() + str(self.number) if self.pvalue != 20 else "rk"

    def __gt__(self, other):
        if self.trump and not other.trump:
            return True
        elif not self.trump and other.trump:
            return False
        elif self.trump:
            return self.tvalue > other.tvalue
        else:
            return self.tvalue > other.tvalue

    def __lt__(self, other):
        if self.trump and not other.trump:
            return False
        elif not self.trump and other.trump:
            return True
        elif self.trump:
            return self.tvalue < other.tvalue
        else:
            return self.tvalue < other.tvalue

    def __eq__(self, other):
        return self.tvalue == other.tvalue

    def __repr__(self):
        return self.short_name()

    def __str__(self):
        return self.short_name()


class Trick:
    def __init__(
        self,
        number: int,
        first_card: Card = None,
        second_card: Card = None,
        thrid_card: Card = None,
        forth_card: Card = None,
        winning_card: Card = None,
        winning_player: Player = None,
    ):
        self.number = number
        # this is important because first card the others must follow suit
        self.first_card = first_card

        self.second_card = second_card

        self.third_card = thrid_card

        self.forth_card = forth_card

        self.winning_card = winning_card

        self.winning_player = winning_player

        self.point_value = 0

    def find_points(self):
        all_cards = self.make_trick_cards()
        points = sum(x.pvalue for x in all_cards)
        self.point_value = points

    def make_trick_cards(self):
        return [
            self.first_card,
            self.second_card,
            self.third_card,
            self.forth_card,
        ]

    def print_trick(self):
        all_cards = self.make_trick_cards()
        print("Trick Summary")
        for x in all_cards:
            trick_str = f"Team {str(x.owner.team)} {x.owner.name} played {x.suit} {str(x.number)}"
            if x.owner == self.winning_player:
                trick_str += " TRICK WINNER"
            print(trick_str)

    def winning_pair(self):
        winning_card = self.first_card
        lead_suit = self.first_card.suit
        all_cards = self.make_trick_cards()
        # determine the winning card using the card object comparison
        for x in all_cards:
            if x.suit == lead_suit and x > winning_card:
                winning_card = x

        self.winning_card = winning_card
        self.winning_player = winning_card.owner

        return self.winning_player


class Round:
    def __init__(self, round_index: int, teams: list[Team], shuffled_deck: list[Card]):
        # values we have at the start
        self.round_index = round_index
        self.team1, self.team2 = teams
        self.players = [
            self.team1.player1,
            self.team1.player2,
            self.team2.player1,
            self.team2.player2,
        ]
        self.deck = shuffled_deck
        # values to be assigned throughout the round
        self.tricks = []
        self.trump = None
        self.lead_player = None
        self.bidding_team = None
        self.winning_bid = None
        self.winning_team = None

    def deal(self):
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            chunked_list = []
            for i in range(0, len(lst), n):
                chunked_list.append(lst[i : i + n])
            return chunked_list

        # distribute cards to players
        hands = chunks(self.deck[:52], 13)

        # assign the dealt cards
        self.dealt_cards = {p.name: hands[idx] for idx, p in enumerate(self.players)}

        # check for re-deal (no pointers in your hand)
        for player_name, hand in self.dealt_cards.items():
            # checks to make sure you have at least one pointer in your hand
            if sum(y.pvalue for y in hand) == 0:
                # to be honest, I think this works, but I am not sure. Hopefully we don't ever run into it.
                self.deck = random.shuffle(self.deck)
                self.deal()

        # order them by suit, and then by tValue
        for player_name, hand in self.dealt_cards.items():
            hand.sort(key=lambda y: [y.suit, y.tvalue], reverse=True)

        # once they have been sorted and we know there isn't a re-deal, assign them to the players
        for idx, p in enumerate(self.players):
            p.set_hand(hands[idx])

        # the widow is the last remaining 5 cards
        self.starting_widow = self.deck[52:]
        self.dealt_cards["widox"] = self.starting_widow

        self.widow = self.starting_widow.copy()

    def bidding_round(self):
        pass

    def assign_trump(self, trump_suit: str):
        """
        Assigns the trump suit to the cards in the players hands
        """
        self.trump = trump_suit
        for x in self.players:
            for y in x.hand:
                # also assign each card to its owner
                y.owner = x
                if y.suit in [self.trump_suit, "Rook"]:
                    y.trump = True

    def play_trick(self, trick_idx: int):
        pass

    def determine_round_winner(self) -> Player:
        pass

    def start(self):
        # deal cards: returns list of lists. Order -> 1,2,3,4, widow
        self.deal()

        # bidding sequence
        self.bidding_round()

        self.show_widow()
        # add widow to winning bidder's hand
        # self.winning_bid.player.hand.extend(self.widow)
        # winning player removes 5 cards from their hand and adds them to the widow
        # self.widow.extend(self.winning_bid.player.remove_widow())
        self.assign_trump(trump_value)

        for trick_count in range(13):
            self.play_trick(trick_count)

        return self.determine_round_winner()


class Bid:
    def __init__(self, bid: int, player: Player):
        if bid in range(100, 181, 5):
            self.bid = bid
        else:
            raise ValueError("Bid must be between 100 and 180 in increments of 5")
        self.player = player

    def __repr__(self):
        return f"{self.player} bid {self.bid}"
