import copy
import game_state
import utilities
from player import BasePlayer

# probability of rolling each value
prob = [.0625, .25, .375, .25, .0625]


class LookAheadAIPlayer(BasePlayer):
    def __init__(self, score_func):
        self.score_func = score_func

    @property
    def name(self):
        return "Look Ahead AI Player ({})".format(self.score_func.__name__)

    def get_move(self, roll, valid_moves, state, player_idx):
        slim_state = game_state.SlimGameState(state)
        move_scores = [0 for _ in valid_moves]

        # Loop through each of our valid moves
        for i, move in enumerate(valid_moves):
            new_state = copy.deepcopy(slim_state)
            new_state.move(move, move + roll, player_idx)

            # will hold the expected score for each possible roll (0, 1, 2, 3, 4), weighted by the probability of
            # that roll occurring
            expected_score_for_roll = [0.0 for _ in prob]

            # Loop through possible opponent rolls,
            # skipping the first because there are no valid moves for a roll of 0
            for opp_roll, p in enumerate(prob[1:]):
                opp_valid_moves_for_roll = new_state.get_valid_moves(1-player_idx, opp_roll)
                if len(opp_valid_moves_for_roll) == 0:
                    continue

                # Stores the scores for each valid opponent move for the current roll
                scores_opp_moves = [0 for _ in opp_valid_moves_for_roll]

                # Loop through valid moves for the current roll
                for idx, opp_move in enumerate(opp_valid_moves_for_roll):
                    opp_state = copy.deepcopy(new_state)
                    opp_state.move(opp_move, opp_move + opp_roll, 1-player_idx)
                    scores_opp_moves[idx] = self.score_func(opp_state, player_idx)

                expected_score_for_roll[opp_roll] = min(scores_opp_moves) * p

            # The score for *our* current move is set to the weighted average of the expected score for our
            # opponent's next move.
            move_scores[i] = sum(expected_score_for_roll)

        choice = valid_moves[utilities.max_index(move_scores)]
        return choice

    def feedback(self, won):
        pass

    def clean_up(self):
        pass
