import ur
import player
import scoring_funcs
import os


N = 1000
csv_delimiter = ";"

player_archetypes = [
    [player.RandomAIPlayer],
    # [player.GreedyAIPlayer, scoring_funcs.flat_score],
    # [player.GreedyAIPlayer, scoring_funcs.linear_score],
    [player.GreedyAIPlayer, scoring_funcs.pow1_5_score],
    # [player.GreedyAIPlayer, scoring_funcs.pow2_score],
    # [player.GreedyAIPlayer, scoring_funcs.pow3_score],
    # [player.GreedyAIPlayer, scoring_funcs.focus_rosettes_score],
    # [player.GreedyAIPlayer, scoring_funcs.penalize_start_score],
    [player.GreedyAIPlayer, scoring_funcs.learned_score],
    # [player.LookAheadAIPlayer, scoring_funcs.flat_score, 1],
    # [player.LookAheadAIPlayer, scoring_funcs.linear_score, 1],
    [player.LookAheadAIPlayer, scoring_funcs.pow1_5_score, 1],
    # [player.LookAheadAIPlayer, scoring_funcs.pow2_score, 1],
    # [player.LookAheadAIPlayer, scoring_funcs.pow3_score, 1],
    # [player.LookAheadAIPlayer, scoring_funcs.focus_rosettes_score, 1],
    # [player.LookAheadAIPlayer, scoring_funcs.penalize_start_score, 1],
    [player.LookAheadAIPlayer, scoring_funcs.learned_score, 1],
    # [player.LookAheadAIPlayer, scoring_funcs.flat_score, 2],
    # [player.LookAheadAIPlayer, scoring_funcs.linear_score, 2],
    [player.LookAheadAIPlayer, scoring_funcs.pow1_5_score, 2],
    # [player.LookAheadAIPlayer, scoring_funcs.pow2_score, 2],
    # [player.LookAheadAIPlayer, scoring_funcs.pow3_score, 2],
    # [player.LookAheadAIPlayer, scoring_funcs.focus_rosettes_score, 2],
    # [player.LookAheadAIPlayer, scoring_funcs.penalize_start_score, 2],
    [player.LookAheadAIPlayer, scoring_funcs.learned_score, 2]
]


def main():
    results_path = os.path.join(os.getcwd(), "all_pairs_results")
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    f = open(os.path.join(results_path, "results.csv"), "w+")

    f.write(" {}".format(csv_delimiter))
    for idx, p in enumerate(player_archetypes):
        f.write(p[0](*p[1:]).name)
        if idx != len(player_archetypes) - 1:
            f.write("{}".format(csv_delimiter))
    f.write("\n")

    for p1_a in player_archetypes:
        p1 = p1_a[0](*p1_a[1:])
        f.write("{}{}".format(p1.name, csv_delimiter))
        for idx, p2_a in enumerate(player_archetypes):
            p2 = p2_a[0](*p2_a[1:])
            players = [p1, p2]
            winner, win_rate = ur.run_game_sequence(players, N)
            f.write("{:.3f}".format(win_rate if winner is p1 else 1-win_rate))
            if idx != len(player_archetypes) - 1:
                f.write("{}".format(csv_delimiter))
        f.write("\n")

    f.close()


if __name__ == '__main__':
    main()
