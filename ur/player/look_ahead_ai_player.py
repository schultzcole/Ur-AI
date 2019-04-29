import copy
import game_state
import utilities
from player import BasePlayer

# probability of rolling each value
prob = [.0625, .25, .375, .25, .0625]


class LookAheadAIPlayer(BasePlayer):
    def __init__(self, score_func, depth):
        self.score_func = score_func
        self.depth = depth

    @property
    def name(self):
        return "Look Ahead AI Player ({}, depth {})".format(self.score_func.__name__, self.depth)

    def get_move(self, roll, valid_moves, state, player_idx):
        slim_state = game_state.SlimGameState(state)
        move_scores = [0 for _ in valid_moves]

        # Loop through each of our valid moves
        for i, move in enumerate(valid_moves):
            new_state = copy.deepcopy(slim_state)
            new_state.move(move, move + roll, player_idx)

            # The score for *our* current move is set to the weighted average of the expected score for our
            # opponent's next move.
            move_scores[i] = sum(self._look_ahead(new_state, player_idx, player_idx, self.depth))

        choice = valid_moves[utilities.max_index(move_scores)]
        return choice

    def _look_ahead(self, state, curr_player_idx, calling_player_idx, remaining_depth):
        curr_state_score = self.score_func(state, calling_player_idx)

        # will hold the expected score for each possible roll (0, 1, 2, 3, 4), weighted by the probability of
        # that roll occurring.
        expected_score_for_roll = [0.0 for _ in prob]

        # Loop through possible opponent rolls,
        # skipping the first because there are no valid moves for a roll of 0
        for next_roll, p in enumerate(prob):
            valid_moves_for_next_roll = state.get_valid_moves(1 - curr_player_idx, next_roll)

            # if there are no valid moves for this roll, proceed to the next layer with the current state
            if len(valid_moves_for_next_roll) == 0:
                if remaining_depth > 1:
                    expected_score_for_roll[next_roll] = sum(
                        self._look_ahead(state, 1 - curr_player_idx, calling_player_idx, remaining_depth - 1)) * p
                else:
                    expected_score_for_roll[next_roll] = curr_state_score * p
                continue

            # Stores the scores for each valid opponent move for the current roll
            scores_next_moves = [0 for _ in valid_moves_for_next_roll]

            # Loop through valid moves for the current roll
            for idx, next_move in enumerate(valid_moves_for_next_roll):
                next_state = copy.deepcopy(state)
                next_state.move(next_move, next_move + next_roll, 1 - curr_player_idx)
                if remaining_depth > 1:
                    scores_next_moves[idx] = sum(
                        self._look_ahead(next_state, 1 - curr_player_idx, calling_player_idx, remaining_depth - 1))
                else:
                    scores_next_moves[idx] = self.score_func(next_state, calling_player_idx)

            if curr_player_idx == calling_player_idx:
                expected_score_for_roll[next_roll] = min(scores_next_moves) * p
            else:
                expected_score_for_roll[next_roll] = max(scores_next_moves) * p

        return expected_score_for_roll

    def feedback(self, won):
        pass

    def clean_up(self):
        pass
