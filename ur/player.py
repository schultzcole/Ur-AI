from abc import ABC, abstractmethod
import random


class Player(ABC):
    def __init__(self, player_id):
        self.player_id = player_id

    @abstractmethod
    def get_move(self, valid_moves):
        """
        Gets the move from this player, given a list of valid moves
        :return: the tile to move from
        """
        pass

    @property
    @abstractmethod
    def _name(self):
        return "Default Player"

    @property
    def name(self):
        return "{} (Player {})".format(self._name, self.player_id + 1)


class HumanPlayer(Player):
    def get_move(self, valid_moves):
        return int(input())

    @property
    def _name(self):
        return "Human Player"


class RandomAIPlayer(Player):
    def get_move(self, valid_moves):
        selection = random.choice(valid_moves)
        return selection

    @property
    def _name(self):
        return "Random AI Player"
