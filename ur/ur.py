import game_board
import game_state as gstate
from functools import reduce
import operator
import random


def main():
    state = gstate.GameState(7)
    game_board.render_board(state)

    print()

    print("Current state is valid? ", state.is_valid())
    current_player = 0
    turn = 0
    while state.won() is None:
        roll = reduce(operator.add, (random.randint(0, 1) for _ in range(4)))
        print("Turn {}".format(turn))

        while True:
            if roll == 0:
                print("Player {}, you rolled a {}. Too bad!".format(current_player + 1, roll))
                break
            source = int(input("Player {}, you rolled a {}. choose a piece to move: ".format(current_player + 1, roll)))

            try:
                state.move(source, source + roll, current_player)
                game_board.render_board(state)
                break
            except gstate.InvalidMoveException:
                print("Invalid Move")

        current_player = 1-current_player
        turn += current_player


if __name__ == '__main__':
    main()
