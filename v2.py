from termcolor import colored


class PathFinder():
    def __init__(self, maze, start, end, wall_char="l", node_char="N", walkable_char="O", path_char="X"):
        self.maze = maze
        self.start = Node(None, start)
        self.end = Node(None, end)

        self.open_list = [self.start]
        self.closed_list = []

        self.height = len(maze)
        self.width = len(maze[0])

        self.wall_char = wall_char
        self.node_char = node_char
        self.walkable_char = walkable_char
        self.path_char = path_char

        self.path = []

    def solve(self):
        # While the open list is not empty
        while len(self.open_list) > 0:

            current_node = self.open_list[0]
            current_index = 0
            # b) pop q off the open list
            for index, node in enumerate(self.open_list):
                if node.F < current_node.F:
                    current_node = node
                    current_index = index

            self.open_list.pop(current_index)
            self.closed_list.append(current_node)
            current_node.print_node()

            # Check if the maze has been solved
            if current_node == self.end:
                current = current_node
                while current:
                    self.path.append(current.position)
                    current = current.parent
                self.path = self.path[::-1]
                return True

            childs = []
            # generate q's 8 successors and set their parents to q
            for pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                new_pos = (current_node.position[0] + pos[0],
                           current_node.position[1] + pos[1])

                # Check if the cell is outside of the maze
                if new_pos[0] > self.height - 1 or new_pos[0] < 0 or new_pos[1] > self.width - 1 or new_pos[1] < 0:
                    continue

                # If the cell is not walkable, return
                if self.maze[new_pos[0]][new_pos[1]] != self.walkable_char and self.maze[new_pos[0]][new_pos[1]] != self.node_char:
                    continue
                
                # Check if the neighbour already is in the closed list
                if Node(current_node, new_pos) in self.closed_list:
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
                self.open_list.append(child)
        return False

    def print_board(self):
        if len(self.path) > 0:
            for item in self.path:
                self.maze[item[0]][item[1]] = self.path_char

        self.maze[self.start.position[0]][self.start.position[1]] = self.node_char
        self.maze[self.end.position[0]][self.end.position[1]] = self.node_char

        for row in self.maze:
            for index, col in enumerate(row):
                if index == len(row)-1:
                    # if col == self.path_char or col == self.node_char:
                    #     print(colored(col, 'green'))
                    # elif col == 'l':
                    #     print(colored(col, 'red'))
                    # else:
                        print(col)
                else:
                    # if col == self.path_char or col == self.node_char:
                    #     print(colored(col, 'green'), end=" ")
                    # elif col == 'l':
                    #     print(colored(col, 'red'), end=" ")
                    # else:
                        print(col, end="  ")


class Node():
    def __init__(self, parent=None, position: tuple = None):
        self.parent = parent
        self.position = position

        self.H = 0
        self.G = 0
        self.F = self.G + self.H

    def __eq__(self, value):
        return self.position == value.position
    
    def print_node(self):
        print('New point: ', self.position, 'G =',self.G,'H =', self.H, 'F = G + H', self.F,)


if __name__ == "__main__":
    # l's represent walls, O's are 'walkable'
    field = [
        ['O', 'l', 'O', 'O', 'O'],
        ['O', 'l', 'O', 'O', 'O'],
        ['O', 'l', 'l', 'l', 'O'],
        ['O', 'O', 'O', 'l', 'O'],
        ['O', 'l', 'O', 'O', 'O']
    ]

    start = (0, 0)
    end = (0, 4)

    wall_char = "l"
    node_char = "N"
    walkable_char = "O"
    path_char = "X"



    finder = PathFinder(field, start, end, wall_char, node_char, walkable_char, path_char)
    print('Starting state')
    finder.print_board()
    if finder.solve():
        print('End state')
        finder.print_board()
    else:
        print("The board couldn't be solved, please make sure the path is open")
