import game_state


def naive_score_full_state(state: game_state.GameState, player):
    tile_scores = [x for x in range(len(state.tiles))]

    player_score = 0
    other_score = 0

    for i, t in enumerate(state.tiles):
        player_score += t.players[player] * tile_scores[i]
        other_score += t.players[1-player] * tile_scores[i]

    return player_score - other_score


def naive_score(state: game_state.SlimGameState, player):
    tile_scores = [x for x in range(len(state.state))]

    player_score = 0
    other_score = 0

    for i, p in state.state.items():
        player_score += p[player] * tile_scores[i]
        other_score += p[1-player] * tile_scores[i]

    return player_score - other_score


def test():
    pass


if __name__ == "__main__":
    test()
