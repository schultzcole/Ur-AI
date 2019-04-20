import game_board
import game_state
from functools import reduce
import operator
import random
import player
from stopwatch import Stopwatch
import scoring_funcs

PRINT_MOVES = False
N = 1000
PIECES = 4


def main():
    player_pairs = [
        # [player.RandomAIPlayer(0), player.GreedyAIPlayer(1, scoring_funcs.flat_score)],
        [player.RandomAIPlayer(), player.RandomAIPlayer()],
        [player.RandomAIPlayer(), player.GreedyAIPlayer(scoring_funcs.linear_score)],
        [player.RandomAIPlayer(), player.GreedyLearningAIPlayer()],
        # [player.RandomAIPlayer(), player.GreedyAIPlayer(scoring_funcs.focus_rosettes_score)],
        # [player.RandomAIPlayer(), player.GreedyAIPlayer(scoring_funcs.penalize_start_score)],
    ]

    for pair in player_pairs:
        run_game_sequence(pair)


def run_game_sequence(players):
    sw = Stopwatch()
    sw.restart()

    wins = {players[0]: 0, players[1]: 0}

    for n in range(N):
        winner = run_game(players)
        players[winner].feedback(True)
        players[1-winner].feedback(False)
        wins[players[winner]] += 1
        players.reverse()

    sw.stop()

    print("Ran {} games in {:.4f}s".format(N, sw.duration))

    for key, val in wins.items():
        print("{} won {} times ({:.2f}%)!".format(key.name, val, val/N*100))

    print()


def run_game(players):
    state = game_state.GameState(PIECES)
    turn = 0

    while state.won() is None:
        output()
        output("-" * 8)
        output("Turn {}".format(turn))
        for idx, p in enumerate(players):
            continue_turn = True
            while continue_turn:
                continue_turn = False

                print_state(state)

                roll = reduce(operator.add, (random.randint(0, 1) for _ in range(4)))
                valid_moves = state.get_valid_moves(idx, roll)

                if roll == 0:
                    output("Player {}, you rolled a {}. Better luck next time!".format(idx + 1, roll))
                    continue

                if len(valid_moves) == 0:
                    output("Player {}, you rolled a {}. There are no valid moves with that roll."
                           "Better luck next time!".format(idx + 1, roll))
                    continue

                output("Player {}, you rolled a {}. Valid moves are {}."
                       "\nChoose a piece to move: ".format(idx + 1, roll, valid_moves), end="")

                while True:
                    try:
                        source = p.get_move(roll, valid_moves, state, idx)
                    except ValueError:
                        output("Invalid input, try again: ", end="")
                        continue

                    try:
                        if state.move(source, source + roll, idx):
                            output("Player {} landed on a rosette! Roll again!".format(idx + 1))
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
