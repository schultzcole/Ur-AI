import game_board
import game_state as gstate
from functools import reduce
import operator
import random


def main():
    state = gstate.GameState(7)

    current_player = 0
    turn = 0
    while state.won() is None:
        print("-"*8)
        print("Player 1 | start: {}; finish: {}".format(state.tiles[0].players[0], state.tiles[-1].players[0]))
        game_board.render_board(state)
        print("Player 2 | start: {}; finish: {}".format(state.tiles[0].players[1], state.tiles[-1].players[1]))
        print("-"*8)

        roll = reduce(operator.add, (random.randint(0, 1) for _ in range(4)))
        print("Turn {}".format(turn))

        first = True
        while True:
            if roll == 0:
                print("Player {}, you rolled a {}. Too bad!".format(current_player + 1, roll))
                break

            prompt = ""
            if first:
                prompt = "Player {}, you rolled a {}. choose a piece to move: ".format(current_player + 1, roll)
                first = False

            error_prompt = "Invalid move, try again: "

            try:
                source = int(input(prompt))
            except ValueError:
                print(error_prompt, end="")
                continue

            try:
                state.move(source, source + roll, current_player)
                break
            except gstate.InvalidMoveException:
                print(error_prompt, end="")

        turn += current_player
        current_player = 1 - current_player


if __name__ == '__main__':
    main()
