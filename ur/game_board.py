def render_board(state):
    """
    Renders the given state to the console.
    :param state: The current game state
    :return: None
    """

    no_tile = "⬚"

    first_line = [
        state.tiles[4].token()[0],
        state.tiles[3].token()[0],
        state.tiles[2].token()[0],
        state.tiles[1].token()[0],
        no_tile,
        no_tile,
        state.tiles[-2].token()[0],
        state.tiles[-3].token()[0]
    ]

    second_line = [tile.token() for tile in state.tiles[5:-3]]

    third_line = [
        state.tiles[4].token()[1],
        state.tiles[3].token()[1],
        state.tiles[2].token()[1],
        state.tiles[1].token()[1],
        no_tile,
        no_tile,
        state.tiles[-2].token()[1],
        state.tiles[-3].token()[1]
    ]

    print("-"*8)
    print("".join(first_line))
    print("".join(second_line))
    print("".join(third_line))
    print("-"*8)
