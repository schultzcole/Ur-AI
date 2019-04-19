import game_state

_flat_values = [1] * 16
_linear_values = [x for x in range(1, 17)]


def _generic_list_score(state: game_state.SlimGameState, player, tile_values):
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
    return _generic_list_score(state, player, [pow(x, exponent) for x in _linear_values])


def flat_score(state, player):
    return _generic_list_score(state, player, _flat_values)


def linear_score(state, player):
    return _generic_list_score(state, player, _linear_values)


def pow2_score(state, player):
    return _pow_score(state, player, 2)


def pow1_5_score(state, player):
    return _pow_score(state, player, 1.5)


def pow3_score(state, player):
    return _pow_score(state, player, 3)
