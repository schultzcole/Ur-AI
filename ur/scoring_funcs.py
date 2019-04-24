import game_state

__rosette_locations = [4, 8, 13]
__start_loc = 0
__end_loc = 15

_flat_values = [1] * 16
_linear_values = [x for x in range(__start_loc, __end_loc + 1)]
_focus_rosettes_values = [(x ** 2) if x not in __rosette_locations else (x ** 2) * 2
                          for x in range(__start_loc, __end_loc + 1)]
_penalize_start_values = [x ** 2 if x != __start_loc else -10 for x in range(__start_loc, __end_loc + 1)]
_learned_values = [0.526, -0.347, 3.849, 2.402, 6.648, 4.627, 6.000, 7.297, 10.813, 7.080, 6.949, 10.294, 8.088, 12.688, 13.205, 15.465]
_learned_vs_learner_values = [0.000, 0.785, 3.558, 3.000, 1.909, 5.000, 5.880, 7.000, 8.361, 9.756, 8.605, 11.000, 11.245, 13.000, 12.973, 15.235]


def generic_list_score(state: game_state.SlimGameState, player, tile_values):
    """
    Takes the current state (as a SlimGameState), a player, and a list of score values for each tile and provides
    a score for that state
    :param state: The current game state (in SlimGameState form)
    :param player: The index of the current player
    :param tile_values: A list of score values assigned to each tile on the game board
    :return: The total score for this state, according to the tile_scores list
    """
    player_score = 0
    other_score = 0

    for i, p in state.state.items():
        player_score += p[player] * tile_values[i]
        other_score += p[1-player] * tile_values[i]

    return player_score - other_score


def _pow_score(state, player, exponent):
    """
    Takes the current state, a player index, and an exponent
    and gives a state score by applying the given exponent to a linear value scale
    :param state: The current state (SlimGameState)
    :param player: The current player index
    :param exponent: The exponent to raise the value to
    :return: Total score for this state
    """
    return generic_list_score(state, player, [pow(x, exponent) for x in _linear_values])


def flat_score(state, player):
    """ Every tile gets the same score """
    return generic_list_score(state, player, _flat_values)


def linear_score(state, player):
    """ A linear scale from start to end node """
    return generic_list_score(state, player, _linear_values)


def pow2_score(state, player):
    """ Power scale, exponent 2 """
    return _pow_score(state, player, 2)


def pow1_5_score(state, player):
    """ Power scale, exponent 1.5 """
    return _pow_score(state, player, 1.5)


def pow3_score(state, player):
    """ Power scale, exponent 3 """
    return _pow_score(state, player, 3)


def focus_rosettes_score(state, player):
    """ Power scale, exponent 2.
    Rosettes have 2x value compared to regular tiles """
    return generic_list_score(state, player, _focus_rosettes_values)


def penalize_start_score(state, player):
    """ Power scale, exponent 2.
    Start tile has substantial negative value to encourage the AI to move pieces onto the board """
    return generic_list_score(state, player, _penalize_start_values)


def learned_score(state, player):
    return generic_list_score(state, player, _learned_values)


def learned_vs_learner_score(state, player):
    return generic_list_score(state, player, _learned_vs_learner_values)
