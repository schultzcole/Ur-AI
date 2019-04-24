from player import BasePlayer


class HumanPlayer(BasePlayer):
    @property
    def name(self):
        return "Human Player"

    def get_move(self, roll, valid_moves, state, player_idx):
        return int(input())

    def feedback(self, won):
        pass

    def clean_up(self):
        pass
