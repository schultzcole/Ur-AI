import math
import copy
import random
import scoring_funcs
from player import GreedyAIPlayer


class GreedyLearningAIPlayer(GreedyAIPlayer):
    class TreeNode:
        def mutate(self, values):
            new_values = copy.copy(values)

            for i in range(self._mutation_rate):
                mutate_idx = random.randrange(len(new_values))
                new_values[mutate_idx] += random.triangular(-self._mutation_range, self._mutation_range, 0)

            return new_values

        def __init__(self, parent, mutation_rate=1, mutation_range=3):
            self._parent = parent
            self._children = []
            self._wins = 0
            self._times = 0
            self._mutation_rate = mutation_rate
            self._mutation_range = mutation_range
            self.tile_values = [x for x in range(16)]

            if parent is not None:
                self.tile_values = self.mutate(parent.tile_values)

        @property
        def win_rate(self):
            if self._times == 0:
                return float("-inf")
            return self._wins / self._times

        def propagate_game(self, won):
            if won:
                self._wins += 1

            self._times += 1
            if self._parent is not None:
                self._parent.propagate_game(won)

        def upper_confidence_bound(self):
            if self._times == 0:
                return 0
            return self._wins / self._times + math.sqrt(2 * math.log(self._parent._times) / self._times)

        def add_child(self):
            child = GreedyLearningAIPlayer.TreeNode(self, self._mutation_rate, self._mutation_range)
            self._children.append(child)
            return child

        def select_in_descendants(self):
            if len(self._children) == 0:
                return self

            max_ucb = 0
            max_idx = 0
            for i, child in enumerate(self._children):
                curr_ucb = child.upper_confidence_bound()
                if curr_ucb > max_ucb:
                    max_ucb = curr_ucb
                    max_idx = i

            return self if self._parent is not None and self.upper_confidence_bound() > max_ucb else \
                self._children[max_idx].select_in_descendants()
            # return self._children[max_idx].select_in_descendants()

        def winningest_brain(self):
            if len(self._children) == 0:
                return self

            best_so_far = self._children[0]

            for i, child in enumerate(self._children):
                best = child.winningest_brain()

                if best.win_rate == best_so_far.win_rate:
                    if best._times > best_so_far._times:
                        best_so_far = best
                elif best.win_rate > best_so_far.win_rate:
                    best_so_far = best

            return self if self.win_rate > best_so_far.win_rate else best_so_far

        def display_tree_stats(self):
            print(len(self._children))

            for child in self._children:
                child.display_tree_stats()

    def score(self, state, player):
        return scoring_funcs.generic_list_score(state, player, self._brain.tile_values)

    def __init__(self, mutation_rate=1, mutation_range=3):
        self._tree_root = GreedyLearningAIPlayer.TreeNode(None, mutation_rate, mutation_range)
        self._brain = self._tree_root
        super().__init__(self.score)

    @property
    def name(self):
        return "Greedy Learning AI Player"

    def feedback(self, won):
        self._brain.propagate_game(won)
        self._brain = self._tree_root.select_in_descendants().add_child()

    def clean_up(self):
        print("Best brain:\n[", end="")

        for i, val in enumerate(self.get_best_brain().tile_values):
            print("{:.3f}{}".format(val, "" if i == 15 else ", "), end="")

        print("]")

    def get_best_brain(self):
        return self._tree_root.winningest_brain()
