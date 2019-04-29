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

            # The score for *our* current move is set to the weighted average of the expected score for our
            # opponent's next move.
            move_scores[i] = sum(self._look_ahead(roll, new_state, player_idx, player_idx, 2))

        choice = valid_moves[utilities.max_index(move_scores)]
        return choice

    def _look_ahead(self, roll, state, curr_player_idx, calling_player_idx, remaining_depth):
        # will hold the expected score for each possible roll (0, 1, 2, 3, 4), weighted by the probability of
        # that roll occurring.
        expected_score_for_roll = [0.0 for _ in prob]
        # immediately set the expected score for a roll of 0 to the score of the current state, as if the
        # opponent rolls a 0 the state will remain the same.
        expected_score_for_roll[0] = self.score_func(state, calling_player_idx) * prob[0]

        # Loop through possible opponent rolls,
        # skipping the first because there are no valid moves for a roll of 0
        for next_roll, p in enumerate(prob[1:]):
            valid_moves_for_next_roll = state.get_valid_moves(1 - curr_player_idx, next_roll)
            if len(valid_moves_for_next_roll) == 0:
                continue

            # Stores the scores for each valid opponent move for the current roll
            scores_opp_moves = [0 for _ in valid_moves_for_next_roll]

            # Loop through valid moves for the current roll
            for idx, next_move in enumerate(valid_moves_for_next_roll):
                next_state = copy.deepcopy(state)
                next_state.move(next_move, next_move + next_roll, 1 - curr_player_idx)
                if remaining_depth > 1:
                    scores_opp_moves[idx] = sum(
                        self._look_ahead(roll, next_state, 1 - curr_player_idx, calling_player_idx, remaining_depth - 1))
                else:
                    scores_opp_moves[idx] = self.score_func(next_state, calling_player_idx)

            if curr_player_idx == calling_player_idx:
                expected_score_for_roll[next_roll] = min(scores_opp_moves) * p
            else:
                expected_score_for_roll[next_roll] = max(scores_opp_moves) * p

        return expected_score_for_roll

    def feedback(self, won):
        pass

    def clean_up(self):
        pass
