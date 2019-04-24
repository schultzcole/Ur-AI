from abc import ABC, abstractmethod


class BasePlayer(ABC):
    @property
    @abstractmethod
    def name(self):
        return "Default Player"

    @abstractmethod
    def get_move(self, roll, valid_moves, state, player_idx):
        """
        Gets the move from this player, given a list of valid moves
        :param roll: The roll the player made for this move
        :param valid_moves: A list of valid move sources
        :param state: The current game state
        :param player_idx: The index of this player
        :return: The chosen move source tile
        """
        pass

    @abstractmethod
    def feedback(self, won):
        """
        Called upon a game's completion to provide feedback to an AI player
        :param won: Whether this player won the game
        :return: None
        """
        pass

    @abstractmethod
    def clean_up(self):
        """
        Called once a game series involving this player has completed.
        :return: None
        """
        pass
