import player
import ur
from anytree import Node
from anytree.exporter import DotExporter

N = 100
PIECES = 4

tree_nodes = []

best_brain = None
best_idx = -1


def create_anytree(curr, parent):
    global best_brain
    global best_idx

    node = Node("{}: {}/{}".format(len(tree_nodes), curr._wins, curr._times), parent=parent)
    tree_nodes.append(node)

    if curr is best_brain:
        best_idx = len(tree_nodes) - 1

    for child in curr._children:
        create_anytree(child, node)


def main():
    global best_brain

    players = [player.RandomAIPlayer(),
               player.GreedyLearningAIPlayer()]
    ur.run_game_sequence(players, N)
    best_brain = players[1].get_best_brain()

    create_anytree(players[1]._tree_root, None)

    print("Best is index {}".format(best_idx))

    DotExporter(tree_nodes[0], graph="strict digraph").to_picture("tree.png")


if __name__ == '__main__':
    main()
