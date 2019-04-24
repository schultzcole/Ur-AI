import copy
import game_state
import utilities
from player import BasePlayer


class GreedyAIPlayer(BasePlayer):
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

    def feedback(self, won):
        pass

    def clean_up(self):
        pass
