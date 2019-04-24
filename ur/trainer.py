import player.greedy_learning_ai_player
from player import base_player
import ur
import os

N = 100000
PIECES = 4


def main():
    players = [player.greedy_learning_ai_player.GreedyLearningAIPlayer(), player.greedy_learning_ai_player.GreedyLearningAIPlayer()]
    best, winrate = ur.run_game_sequence(players, N)

    f = open(os.path.join(os.getcwd(), "training_results", "results.txt"), "a+")

    output = ["{:.3f}: [".format(winrate)]
    for i, val in enumerate(best.get_best_brain().tile_values):
        output.append("{:.3f}{}".format(val, ", " if i < 15 else ""))
    output.append("]\n")
    f.write("".join(output))
    f.close()


if __name__ == '__main__':
    main()
