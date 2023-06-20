from game_play.game_objects import Round, Team, Player
import game_play.preprocessing as pp
import game_play.team_maker as tm
import datetime as dt
from typing import Optional


class Game:
    """
    Game class for Rook
    This contains everything you will need for a game of Rook
    First to 500 points wins
    """

    def __init__(self):
        # set the game ID
        self.game_id: int = int(dt.datetime.now().timestamp())
        # pull in the card pool, we will be using this frequently
        self.card_pool: list = pp.make_deck_list()

        # determine the players and team objects
        # assigns values to self.players, self.team1, self.team2
        self.determine_players()
        self.determine_teams()

        self.rounds = []
        self.round_number = 0
        self.winning_team = None

    def determine_players(self):
        players = tm.get_players()
        self.players = [Player(p, idx) for idx, p in enumerate(players.keys())]

    def determine_teams(self):
        self.team1 = Team(self.players[0], self.players[1])
        self.team2 = Team(self.players[2], self.players[3])

    def check_for_game_winner(self) -> bool:
        """
        Checks to see if a team has won the game
        :return: bool
        """
        if self.team1 > self.team2 & self.team1.game_score >= 500:
            self.winning_team = self.team1
            return True
        elif self.team2 > self.team1 & self.team2.game_score >= 500:
            self.winning_team = self.team2
            return True
        else:
            return False

    def start(self):
        while self.winning_team is None:
            self.round_number += 1
            current_round = Round(
                self.round_number,
                [self.team1, self.team2],
                pp.shuffle_deck(self.card_pool.copy()),
            )
            current_round.start()
            self.rounds.append(current_round)
            self.check_for_game_winner()
