from itertools import product

# 1's represent walls, 0's are 'walkable'
field = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0]
]


class PathFinder():
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = Node(None, start)
        self.end = Node(None, end)

        self.open_list = [self.start]
        self.closed_list = []

        self.height = len(maze)
        self.width = len(maze[0])

    def solve(self):
        # 3.  while the open list is not empty
        while len(self.open_list) > 0:

            current_node = self.open_list[0]
            current_index = 0
            # b) pop q off the open list
            for index, node in enumerate(self.open_list):
                if node == current_node:
                    current_node = node
                    current_index = index

            self.open_list.pop(current_index)
            self.closed_list.append(current_node)

            # Check if the maze has been solved
            if current_node == self.end:
                path = []
                current = current_node
                while current:
                    path.append(current)
                    current = current.parent
                return path[::-1]

            childs = []
            # c) generate q's 8 successors and set their parents to q
            for pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                new_pos = (current_node.position[0] + pos[0],
                           current_node.position[1] + pos[1])

                # Check if the cell is outside of the maze
                if new_pos[0] > self.height - 1 or new_pos[0] < 0 or new_pos[1] > self.width - 1 or new_pos[1] < 0:
                    continue

                # If the cell is not walkable, return
                if self.maze[new_pos[0]][new_pos[1]] != 0:
                    continue

                childs.append(Node(current_node, new_pos))

            for child in childs:
                # Check if the child is already in the closed_list
                for x in self.closed_list:
                    if child == x:
                        continue

                child.G = current_node.G + 1

                # This should be a square root but this is easier :)))
                child.H = abs(child.position[0] - current_node.position[0])**2 + abs(
                    child.position[1] - current_node.position[1])**2

                child.F = child.G + child.H

                # If there already is a better path to this cell or the child is already in the list , continue
                for x in self.open_list:
                    if child == x and child.G > x.G:
                        continue

               # print('Position found: ', child.position, 'score: ',
                #      child.F, 'Open list lengt: ', len(self.open_list))
                self.open_list.append(child)


class Node():
    def __init__(self, parent=None, position: tuple = None):
        self.parent = parent
        self.position = position

        self.H = 0
        self.G = 0
        self.F = self.G + self.H

    def __eq__(self, value):
        return self.position == value.position


if __name__ == "__main__":
    finder = PathFinder(field, (0, 0), (0, 4))

    print(finder.solve())
