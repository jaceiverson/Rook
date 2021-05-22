import pickle


class Player:
    def __init__(self,
                 name: str = None,
                 num: int = None,
                 hand: list = None,
                 team: int = None,
                 bid: int = 100,
                 location: str = None,
                 socket_obj=None):

        # entered name
        self.name = name
        self.num = num
        # a list of card objects
        self.hand = hand
        # what their max bid was, defaults to 100
        self.bid = bid
        # what team (1/2) the player is on
        self.team = team
        # need to save the location (internet) of player to send things via socket
        self.location = location
        # save the entire socket object of the person
        self.socket_obj = socket_obj

    def show_hand(self):
        # print the list of hands to the console
        self.hand.sort(key=lambda x: [x.suit, x.tvalue], reverse=True)
        print(self.name + '\'s Hand')
        for x in range(len(self.hand)):
            print(x + 1, self.hand[x].suit, self.hand[x].number)

    def available_cards(self, lead_suit: str, count: int, lead_suit_is_trump: bool):
        # determines which cards are available to play each trick
        print('Available Cards to Play')
        available = []
        if count == 1:
            # if this is the first card played this trick
            available = self.hand
            for y in range(len(available)):
                print(str(y + 1) + ' ' + available[y].suit + ' ' + str(available[y].number))
        else:
            for x in range(len(self.hand)):
                if self.hand[x].suit == lead_suit or (self.hand[x].number == 20 and lead_suit_is_trump):
                    available.append(self.hand[x])
            if len(available) == 0:
                for x in range(len(self.hand)):
                    if self.hand[x].trump:
                        available.append(self.hand[x])

            if len(available) == 0:
                print('You can play anything, but it is a non-factor to the trick')
                available = self.hand
            else:
                print('You must play one of the following cards')
                for y in range(len(available)):
                    print(str(y + 1) + ' ' + available[y].suit + ' ' + str(available[y].number))

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
