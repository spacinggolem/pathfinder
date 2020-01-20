from itertools import product

# '' are emptty cells, x represents the nodes
field = [
    ['', '', '1', '', ''],
    ['', 'x', '1', '', ''],
    ['', '', '', '', ''],
    ['', '', '1', '', ''],
    ['', '', '1', '', 'x']
]

# This will contain all the coordinates of the path
path = []

HEIGHT = 5
WIDTH = 5


def main():
    node1, node2 = getNodes(field)

    path.append(node1)

    getBestMove(node1, node2)

    print(path)


def getNodes(field: list):
    result = []

    for c_row, row in enumerate(field):
        for c_cell, cell in enumerate(row):
            if cell == "x":
                result.append([c_row, c_cell])

    if len(result) != 2:
        raise KeyError("Couldn't find 2 nodes :////")

    return result


def find_neigbours(cell):
    for c in product(*(range(n-1, n+2) for n in cell)):
        if c != cell and all(0 <= n < HEIGHT for n in c):
            yield c


def getMoveScore(c_cell, p_cell, desitination):
    if c_cell[0] == p_cell[0] or c_cell[1] == p_cell[1]:
        # If either x or y is the same it is a vertical or horizontal move
        G = 10
    else:
        # If none of the cordinates is the same it is a diagonal move
        G = 14

    # The estimated distance is delta y + delta x: pythgoras
    H = abs(p_cell[0] - desitination[0]) + abs(p_cell[1] - desitination[1])

    F = G + H

    score = Score(F, G, H)

    return score


def getBestMove(c_node, end_node):

    if c_node[0] == end_node[0] and c_node[1] == end_node[1]:
        showResult()
    else:

        neighbours = list(find_neigbours(c_node))

        best_score = Score(0, 0, 0)
        for neighbour in neighbours:
            score = getMoveScore(c_node, neighbour, end_node)
            if field[neighbour[0]][neighbour[1]] == '1':
                continue

            # If this move is more efficient than last move or is the first one
            if score.F < best_score.F or best_score.F == 0:
                best_move = neighbour
                best_score = score

        if getMoveScore(best_move, [best_move[0]+1, best_move[1]], end_node).G < best_score.G:
            best_move = [best_move[0]+1, best_move[1]]

        path.append(best_move)
        print(f"Best move: {best_move} score: {best_score.H}")
        getBestMove(best_move, end_node)


def showResult():
    pass


class Score():
    def __init__(self, F, G, H):
        self.F = F
        self.G = G
        self.H = H


if __name__ == "__main__":
    main()
