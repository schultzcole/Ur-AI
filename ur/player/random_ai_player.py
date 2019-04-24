import random
from player import BasePlayer


class RandomAIPlayer(BasePlayer):
    @property
    def name(self):
        return "Random AI Player"

    def get_move(self, roll, valid_moves, state, player_idx):
        selection = random.choice(valid_moves)
        return selection

    def feedback(self, won):
        pass

    def clean_up(self):
        pass
