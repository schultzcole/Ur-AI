import game_board
import game_state as gstate
from functools import reduce
import operator
import random
import player
from stopwatch import Stopwatch


def main():
    print_moves = False

    n = 10000

    sw = Stopwatch()
    sw.restart()
    wins = {1: 0, 2: 0}

    for i in range(n):
        wins[run_game(print_moves)] += 1

    sw.stop()

    print("\n\n")
    print("Ran {} games in {}s".format(n, sw.duration))

    for key, val in wins.items():
        print("Player {} won {} times!".format(key, val))


def run_game(print_moves):
    state = gstate.GameState(7)
    players = [player.RandomAIPlayer(0), player.RandomAIPlayer(1)]
    turn = 0

    while state.won() is None:
        for p in players:
            if print_moves:
                print_state(state, turn)

            roll = reduce(operator.add, (random.randint(0, 1) for _ in range(4)))
            valid_moves = state.get_valid_moves(p.player_id, roll)

            if roll == 0:
                if print_moves:
                    print("Player {}, you rolled a {}. Better luck next time!".format(p.player_id + 1, roll))
                continue

            if len(valid_moves) == 0:
                if print_moves:
                    print("Player {}, you rolled a {}. There are no valid moves with that roll."
                          "Better luck next time!".format(p.player_id + 1, roll))
                continue

            if print_moves:
                print("Player {}, you rolled a {}. Valid moves are {}."
                      "\nChoose a piece to move: ".format(p.player_id + 1, roll, valid_moves), end="")

            while True:
                source = p.get_move(valid_moves)

                try:
                    state.move(source, source + roll, p.player_id)
                    break
                except gstate.InvalidMoveException:
                    if print_moves:
                        print("Invalid move, try again: ", end="")

        turn += 1

    if print_moves:
        print("\n\nPlayer {} won!".format(state.won()))
        print_board(state)

    return state.won()


def print_state(state, turn):
    print()
    print("-" * 8)
    print("Turn {}".format(turn))
    print_board(state)
    print()


def print_board(state):
    print("Player 1 | start: {}; finish: {}".format(state.tiles[0].players[0], state.tiles[-1].players[0]))
    game_board.render_board(state)
    print("Player 2 | start: {}; finish: {}".format(state.tiles[0].players[1], state.tiles[-1].players[1]))


if __name__ == '__main__':
    main()
