from abc import ABC, abstractmethod
import random
import copy
import utilities
import game_state


class Player(ABC):
    def __init__(self, player_id):
        self.player_id = player_id

    @abstractmethod
    def get_move(self, roll, valid_moves, state):
        """
        Gets the move from this player, given a list of valid moves
        :param roll: The roll the player made for this move
        :param valid_moves: A list of valid move sources
        :param state: The current game state
        :return: The chosen move source tile
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
    def get_move(self, roll, valid_moves, state):
        return int(input())

    @property
    def _name(self):
        return "Human Player"


class RandomAIPlayer(Player):
    def get_move(self, roll, valid_moves, state):
        selection = random.choice(valid_moves)
        return selection

    @property
    def _name(self):
        return "Random AI Player"


class GreedyAIPlayerSlow(Player):
    def __init__(self, player_id, score_func):
        super().__init__(player_id)

        self.score_func = score_func

    def get_move(self, roll, valid_moves, state):
        move_scores = [0 for _ in valid_moves]

        for i, move in enumerate(valid_moves):
            new_state = copy.deepcopy(state)
            new_state.move(move, move + roll, self.player_id)
            move_scores[i] = self.score_func(new_state, self.player_id)

        choice = valid_moves[utilities.max_index(move_scores)]
        return choice

    @property
    def _name(self):
        return "Slow Greedy AI Player ({})".format(self.score_func.__name__)


class GreedyAIPlayer(Player):
    def __init__(self, player_id, score_func):
        super().__init__(player_id)

        self.score_func = score_func

    def get_move(self, roll, valid_moves, state):
        slim_state = game_state.SlimGameState(state)
        move_scores = [0 for _ in valid_moves]

        for i, move in enumerate(valid_moves):
            new_state = copy.deepcopy(slim_state)
            new_state.move(move, move + roll, self.player_id)
            move_scores[i] = self.score_func(new_state, self.player_id)

        choice = valid_moves[utilities.max_index(move_scores)]
        return choice

    @property
    def _name(self):
        return "Greedy AI Player ({})".format(self.score_func.__name__)

