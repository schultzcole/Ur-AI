from abc import ABC, abstractmethod
import random
import copy
import utilities
import game_state
import scoring_funcs


class Player(ABC):
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

    @property
    @abstractmethod
    def name(self):
        return "Default Player"


class HumanPlayer(Player):
    def get_move(self, roll, valid_moves, state, player_idx):
        return int(input())

    @property
    def name(self):
        return "Human Player"


class RandomAIPlayer(Player):
    def get_move(self, roll, valid_moves, state, player_idx):
        selection = random.choice(valid_moves)
        return selection

    @property
    def name(self):
        return "Random AI Player"


class GreedyAIPlayer(Player):
    def __init__(self, score_func):
        self.score_func = score_func

    def get_move(self, roll, valid_moves, state, player_idx):
        slim_state = game_state.SlimGameState(state)
        move_scores = [0 for _ in valid_moves]

        for i, move in enumerate(valid_moves):
            new_state = copy.deepcopy(slim_state)
            new_state.move(move, move + roll, player_idx)
            move_scores[i] = self.score_func(new_state, player_idx)

        choice = valid_moves[utilities.max_index(move_scores)]
        return choice

    @property
    def name(self):
        return "Greedy AI Player ({})".format(self.score_func.__name__)
