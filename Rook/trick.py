from Rook.player import Player
from Rook.card import Card

class Trick:
    def __init__(self,
                 number:int,
                 first_card:Card = None,
                 second_card:Card = None,
                 thrid_card:Card = None,
                 forth_card:Card = None,
                 winning_card:Card = None,
                 winning_player:Player = None):
        self.number=number
        #this is important because first card the others must follow suit
        self.first_card = first_card

        self.second_card = second_card

        self.third_card = thrid_card

        self.forth_card = forth_card

        self.winning_card = winning_card

        self.winning_player=winning_player

        self.point_value=0

    def find_points(self):
        points=0
        all_cards=self.make_trick_cards()
        for x in all_cards:
            points+=x.pvalue

        self.point_value=points

    def make_trick_cards(self):
        all_cards = [self.first_card, self.second_card, self.third_card, self.forth_card]
        return all_cards

    def print_trick(self):
        all_cards=self.make_trick_cards()
        print('Trick Summary')
        for x in all_cards:
            trick_str = f"Team {str(x.owner.team)} {x.owner.name} played {x.suit} {str(x.number)}"
            if x.owner==self.winning_player:
                trick_str += " TRICK WINNER"
            print(trick_str)

    def winning_pair(self):
        winning_card=self.first_card
        lead_suit=self.first_card.suit
        all_cards=self.make_trick_cards()
        for x in all_cards[1:]:

            if x.suit != lead_suit:
            #if played suit is different than lead suit
                if x.trump:
                #if played suit is trump
                    if winning_card.trump:
                    #if current winning_card is trump
                        if x.tvalue>winning_card.tvalue:
                            #if played card is greater than current that is new winner
                            winning_card=x
                    else:
                    #this means played card is trump, but current winning card isn't
                        winning_card=x
                else:
                #this means played suit wasn't lead_suit nor trump, no tvalue to card
                    pass
            elif x.trump:
            #played suit is same as lead and both are trump
                if x.tvalue>winning_card.tvalue:
                    #if tvalue of played card is > than winning card it is new winner
                    winning_card=x

            elif x.trump==False:
                if winning_card.trump:
                    pass
                else:
                    if x.tvalue>winning_card.tvalue:
                        winning_card=x

        self.winning_card=winning_card
        self.winning_player=winning_card.owner

        return self.winning_player
