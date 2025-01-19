import pickle
import random
import tkinter.dnd as dnd
from tkinter import FLAT, SOLID, Button, E, Label, LabelFrame, Tk, W

from PIL import Image, ImageTk


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
        if num in range(1, 5):
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

        # init hand
        if hand is not None:
            self.set_hand(hand)

    def set_hand(self, hand: list) -> None:
        # player hand list of card objects
        if isinstance(hand, list) and len(hand) == 13 and isinstance(hand[0], Card):
            self.hand = Hand(hand)
        else:
            raise ValueError("Hand must be a list of 13 card objects")

    def show_hand(self):
        # print the list of hands to the console
        self.hand.sort()
        print(f"{self.name}'s Hand")
        self.hand.show()

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
        return self.__repr__()


class Card:
    def __init__(
        self,
        suit: str,
        number: int,
        pvalue: int,
        tvalue: int,
        trump: bool = False,
        is_front: bool = True,
    ):
        # VALIDATE ALL THE INPUTS
        # EACH of these will raise a ValueError if the input is not valid
        # if it is valid, it will assign the value to the object
        self.suit = self.suit_validation(suit)
        self.number = self.number_validation(number)
        self.pvalue = self.pvalue_validation(pvalue)
        self.tvalue = self.tvalue_validation(tvalue)
        self.trump = self.trump_validation(trump)

        # each card pertains to a particular player
        self.owner = None

        # this is to show the front or back of the card in the GUI
        self.is_front = is_front

    @property
    def short_name(self):
        # card short name is the first letter of the suit and the number
        # unless the card is a rook, then it is rk
        return self.suit[0].lower() + str(self.number) if self.pvalue != 20 else "rk"

    @staticmethod
    def suit_validation(suit: str) -> str:
        """
        validate suit input
        """
        if suit.lower() in {"red", "green", "yellow", "black", "rook"}:
            return suit.lower()
        else:
            raise ValueError("Suit must be red, green, yellow, black, or rook")

    @staticmethod
    def number_validation(number: int) -> int:
        """
        validate number input
        """
        if number in range(1, 15) or number == 20:
            return number
        else:
            raise ValueError("Number must be between 1 and 14 or 20")

    @staticmethod
    def pvalue_validation(pvalue: int) -> int:
        """
        validate point value input
        """
        if pvalue in {0, 5, 10, 15, 20}:
            return pvalue
        else:
            raise ValueError("Point value must be 0, 5, 10, 15, or 20")

    @staticmethod
    def tvalue_validation(tvalue: int) -> int:
        """
        validate trick value input
        """
        if tvalue in range(2, 16) or tvalue == 20:
            return tvalue
        else:
            raise ValueError("Trick value must be between 2 and 15 or 20")

    @staticmethod
    def trump_validation(trump: bool) -> bool:
        """
        validate trump input
        """
        if trump in {True, False}:
            return trump
        else:
            raise ValueError("Trump must be a boolean object: True or False")

    def __gt__(self, other):
        """
        Compare cards together. Logic of which cards are greater than others

        In this case greater in terms of trick value
        """
        if self.trump and not other.trump:
            return True
        elif not self.trump and other.trump:
            return False
        elif self.suit == other.suit:
            return self.tvalue > other.tvalue
        else:
            return True

    def __lt__(self, other):
        """
        Compare cards together. Logic of which cards are less than others

        This is the direct inverse of the __gt__() method
        """
        if self.trump and not other.trump:
            return False
        elif not self.trump and other.trump:
            return True
        elif self.suit == other.suit:
            return self.tvalue < other.tvalue
        else:
            return False

    def __repr__(self):
        return self.short_name()

    def __str__(self):
        return self.short_name()


class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.top_row = []
        self.bottom_row = []
        self.card_images = []

    def __add__(self, other):
        if isinstance(other, list):
            self.cards.extend(other)
        elif isinstance(other, Card):
            self.cards.append(other)
        elif isinstance(other, Hand):
            self.cards.extend(other.cards)

        return self

    def __len__(self):
        return len(self.cards)

    def show(self):
        root = Tk()
        root.title("Hand")
        root.resizable(False, False)

        # Frame for the buttons.
        btn_frame = LabelFrame(root)
        btn_frame.grid(row=0, column=1)

        # Frame for the two card images.
        cards_frame = LabelFrame(root, pady=4)
        cards_frame.grid(row=1, column=0, padx=10, pady=5)

        # Frame for the card information.
        info_frame = LabelFrame(root)
        info_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=W)

        self.card_buttons = []
        for idx, card in enumerate(self.cards):
            button = Button(cards_frame, command=lambda idx=idx: self.show_back(idx))
            self.card_buttons.append(button)
            front = Image.open(f"./rook/resources/card-img/{card.short_name}.jpg")
            photo = ImageTk.PhotoImage(front.resize((75, 120), Image.BOX))
            button.config(image=photo)
            button.image = photo  # Store reference to the PhotoImage
            button.grid(row=1, column=idx + 1, padx=2, pady=2)
            self.card_images.append(photo)

        show_info_button = Button(
            btn_frame, text="Show Card Info", command=self.submit_cards
        )
        show_info_button.pack()

        drop_card_button = Button(
            btn_frame, text="Drop Cards", command=lambda: (self.submit_cards, self.show)
        )
        drop_card_button.pack()

        self.card_info_label = Label(info_frame, text="")
        self.card_info_label.pack(anchor=W)

        root.mainloop()

    def show_back(self, card_index):
        card = self.cards[card_index]
        if card.is_front:
            back = Image.open("./rook/resources/card-img/back.jpg")
            photo = ImageTk.PhotoImage(back.resize((75, 120), Image.BOX))
        else:
            front = Image.open(f"./rook/resources/card-img/{card.short_name}.jpg")
            photo = ImageTk.PhotoImage(front.resize((75, 120), Image.BOX))

        self.card_buttons[card_index].config(image=photo)
        self.card_buttons[card_index].image = photo

        card.is_front = not card.is_front

    def show_card_info(self):
        visible_cards = [card.short_name for card in self.cards]
        back_facing_cards = [
            card.short_name for card in self.cards if not card.is_front
        ]
        formatted_vis_cards = "\n".join(visible_cards)
        formatted_back_cards = "\n".join(back_facing_cards)
        card_info = f"Visible Cards:\n{formatted_vis_cards}\n\nBack-Facing Cards:\n{formatted_back_cards}"
        self.card_info_label.config(text=card_info)

    def submit_cards(self):
        flipped_cards = [card for card in self.cards if not card.is_front]
        """
        for card in flipped_cards:
            self.cards.remove(card)
        """
        flipped_card_names = [card.short_name for card in flipped_cards]
        print("Flipped Cards:")
        print(flipped_card_names)

    def drop_flipped_cards(self, cards: list):
        """
        remove dropped cards from the hand

        save them to a list to be returned. these are the new widow
        """
        new_widow = [card for card in self.cards if not card.is_front]
        new_hand = [card for card in self.cards if card.is_front]
        self.cards = new_hand
        return new_widow

    def refresh(self):
        """clear the GUI and redraw the cards"""
        pass

    def sort(self):
        """
        Sort the cards in the hand by suit and then by tValue
        """
        self.cards.sort(key=lambda x: [x.suit, x.tvalue], reverse=True)


class Trick:
    def __init__(
        self,
        number: int,
        first_card: Card = None,
        second_card: Card = None,
        third_card: Card = None,
        forth_card: Card = None,
        winning_card: Card = None,
        winning_player: Player = None,
    ):
        self.number = number
        # this is important because first card the others must follow suit
        self.first_card = first_card

        self.second_card = second_card

        self.third_card = third_card

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
            for y in x.hand.cards:
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

        self.players[0].hand.show()

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
