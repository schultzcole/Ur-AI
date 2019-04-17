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


class HumanPlayer(Player):
    def get_move(self, valid_moves):
        return int(input())


class RandomAIPlayer(Player):
    def get_move(self, valid_moves):
        selection = random.choice(valid_moves)
        return selection