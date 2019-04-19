import game_state

_flat_scores = [1] * 16
_linear_scores = [x for x in range(1, 17)]


def _generic_score(state: game_state.SlimGameState, player, tile_scores):
    player_score = 0
    other_score = 0

    for i, p in state.state.items():
        player_score += p[player] * tile_scores[i]
        other_score += p[1-player] * tile_scores[i]

    return player_score - other_score


def _pow_score(state, player, power):
    return _generic_score(state, player, [pow(x, power) for x in _linear_scores])


def flat_score(state, player):
    return _generic_score(state, player, _flat_scores)


def linear_score(state, player):
    return _generic_score(state, player, _linear_scores)


def pow2_score(state, player):
    return _pow_score(state, player, 2)


def pow1_5_score(state, player):
    return _pow_score(state, player, 1.5)


def pow3_score(state, player):
    return _pow_score(state, player, 3)
