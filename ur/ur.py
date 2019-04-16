import game_board
import game_state as gstate
from functools import reduce
import operator
import random
import player
from stopwatch import Stopwatch


def main():

    sw = Stopwatch()
    sw.restart()

    run_game()

    print("Game ran in {}s".format(sw.duration))


def run_game():
    state = gstate.GameState(7)
    players = [player.RandomAIPlayer(0), player.RandomAIPlayer(1)]
    turn = 0

    while state.won() is None:
        for p in players:
            print()
            print("-" * 8)
            print("Turn {}".format(turn))
            print("Player 1 | start: {}; finish: {}".format(state.tiles[0].players[0], state.tiles[-1].players[0]))
            game_board.render_board(state)
            print("Player 2 | start: {}; finish: {}".format(state.tiles[0].players[1], state.tiles[-1].players[1]))
            print()

            roll = reduce(operator.add, (random.randint(0, 1) for _ in range(4)))

            if roll == 0:
                print("Player {}, you rolled a {}. Better luck next time!".format(p.player_id + 1, roll))
                continue

            print("Player {}, you rolled a {}. choose a piece to move: ".format(p.player_id + 1, roll), end="")

            error_count = 0
            while True:
                source = p.get_move(None)

                try:
                    state.move(source, source + roll, p.player_id)
                    break
                except gstate.InvalidMoveException:
                    error_count += 1
                    if error_count == 20:
                        break
                    print("Invalid move, try again: ", end="")

        turn += 1

    print("\n\nPlayer {} won!".format(state.won()))
    print("Player 1 | start: {}; finish: {}".format(state.tiles[0].players[0], state.tiles[-1].players[0]))
    game_board.render_board(state)
    print("Player 2 | start: {}; finish: {}".format(state.tiles[0].players[1], state.tiles[-1].players[1]))

    return state.won()


if __name__ == '__main__':
    main()
