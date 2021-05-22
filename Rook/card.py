from Rook.player import Player
class Card:
    def __init__(self,
                 suit:str = None,
                 number:int = None,
                 pvalue:int = None,
                 tvalue:int = None,
                 trump:bool = False,
                 owner:Player = None):
        # suit of the card object
        self.suit = suit

        # number on the card
        self.number = number

        # Point Value of the card
        self.pvalue=pvalue

        # Trick Value of card
        self.tvalue=tvalue

        #BOOLEAN if the card is trump
        self.trump=trump

        #each card pertains to a particular player
        self.owner=owner

        #card short name
        if self.pvalue!=20:
            self.s_name=self.suit[0].lower()+str(self.number)
        else:
            self.s_name='rk'
