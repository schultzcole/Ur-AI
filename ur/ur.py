import game_board
import game_state
from functools import reduce
import operator
import random
import player
from stopwatch import Stopwatch
import state_score

PRINT_MOVES = False
N = 1000
PIECES = 4


def main():
    sw = Stopwatch()
    sw.restart()
    players = [player.GreedyAIPlayerSlow(0, state_score.naive_score_full_state),
               player.GreedyAIPlayer(1, state_score.naive_score)]
    wins = {0: 0, 1: 0}

    for n in range(N):
        wins[run_game(players)] += 1
        players.reverse()

    sw.stop()

    print("Ran {} games in {}s".format(N, sw.duration))

    for key, val in wins.items():
        print("{} won {} times!".format(players[key].name, val))


def run_game(players):
    state = game_state.GameState(PIECES)
    turn = 0

    while state.won() is None:
        output()
        output("-" * 8)
        output("Turn {}".format(turn))
        for p in players:
            continue_turn = True
            while continue_turn:
                continue_turn = False

                print_state(state)

                roll = reduce(operator.add, (random.randint(0, 1) for _ in range(4)))
                valid_moves = state.get_valid_moves(p.player_id, roll)

                if roll == 0:
                    output("Player {}, you rolled a {}. Better luck next time!".format(p.player_id + 1, roll))
                    continue

                if len(valid_moves) == 0:
                    output("Player {}, you rolled a {}. There are no valid moves with that roll."
                           "Better luck next time!".format(p.player_id + 1, roll))
                    continue

                output("Player {}, you rolled a {}. Valid moves are {}."
                       "\nChoose a piece to move: ".format(p.player_id + 1, roll, valid_moves), end="")

                while True:
                    try:
                        source = p.get_move(roll, valid_moves, state)
                    except ValueError:
                        output("Invalid input, try again: ", end="")
                        continue

                    try:
                        if state.move(source, source + roll, p.player_id):
                            output("Player {} landed on a rosette! Roll again!".format(p.player_id + 1))
                            continue_turn = True
                        break
                    except game_state.InvalidMoveException:
                        output("Invalid move, try again: ", end="")

                if PRINT_MOVES:
                    # time.sleep(.5)
                    pass

            if state.won() is not None:
                break

        turn += 1

    output("\n\nPlayer {} won!".format(state.won()))
    print_board(state)

    output("\n\n")
    return state.won()


def output(o="", end="\n"):
    if PRINT_MOVES:
        print(o, end=end)


def print_state(state):
    if PRINT_MOVES:
        print()
        print_board(state)
        print()


def print_board(state):
    if PRINT_MOVES:
        print("Player 1 | start: {}; finish: {}".format(state.tiles[0].players[0], state.tiles[-1].players[0]))
        game_board.render_board(state)
        print("Player 2 | start: {}; finish: {}".format(state.tiles[0].players[1], state.tiles[-1].players[1]))


if __name__ == '__main__':
    main()
