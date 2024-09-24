from colorama import Fore


def create_maze(filename):
    """
    Reads a maze description file and returns the maze representation, target position,
    and maze dimensions.

    Args:
        filename (str): The path to the maze description file.

    Returns:
        tuple: A tuple containing the following elements:
            - maze (list): A 2D list representing the maze, where ' ' represents a path,
                          'X' represents a wall, and 'E' marks the exit (target).
            - target (tuple): The coordinates (x, y) of the exit (target) in the maze.
            - x_max (int): The maximum x-coordinate (width) of the maze.
            - y_max (int): The maximum y-coordinate (height) of the maze.
            - start_x (int): The x-coordinate of the starting position.
            - start_y (int): The y-coordinate of the starting position.

    Raises:
        FileNotFoundError: If the maze description file is not found.
    """

    try:
        with open(filename, 'r') as file:
            lines = file.read().splitlines()

        maze = []
        target = None
        start_x = None
        start_y = None
        y = -1
        for line in lines:
            y += 1
            maze_line = []
            for i in range(0, len(line), 2):
                if line[i] == 'E':
                    maze_line.append('X')
                    target = (i // 2, y)
                elif line[i] == 'S':
                    maze_line.append(' ')
                    start_x = i // 2
                    start_y = y
                else:
                    maze_line.append(line[i])
            maze.append(maze_line)

        y_max = len(maze) - 1
        x_max = len(maze[0]) - 1

        return maze, target, x_max, y_max, start_x, start_y

    except FileNotFoundError:
        raise FileNotFoundError(f"Maze description file '{filename}' not found.")


def choose_road(crossroads, pos, target):
    """
    Chooses the next step in the maze exploration based on the closest Euclidean
    distance to the target.

    Args:
        crossroads (list): A list of available coordinates (tuples) to explore.
        pos (tuple): The current position (x, y) in the maze.
        target (tuple): The coordinates (x, y) of the exit (target) in the maze.

    Returns:
        tuple: The coordinates (x, y) of the next step to explore.
    """

    min_dist = float('inf')
    closest_cood = None
    for cood in crossroads:
        dist = ((target[0] - cood[0])**2 + (target[1] - cood[1])**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest_cood = cood

    crossroads.remove(closest_cood)
    return closest_cood


class Agent:
    """
    Represents an agent exploring the maze.

    Attributes:
        start (tuple): The starting position (x, y) of the agent.
        pos (tuple): The current position (x, y) of the agent.
        vision (list): A list of visible coordinates (tuples) around the agent.
        past_cood (list): A list of previously visited coordinates (tuples).
        crossroads (list): A list of potential next steps (tuples) for exploration.
    """

    def __init__(self):
        self.start = (0, 0)
        self.pos = (0, 0)
        self.vision = []
        self.past_cood = []
        self.crossroads = []
        self.stuck=False
    
    def rewrite_vis(self, bounds):
        """
        Updates the agent's view of the surrounding cells within the maze boundaries.

        Args:
            bounds (tuple): A tuple containing the maze dimensions (x_max, y_max).

        Returns:
            list: A list of visible coordinates (tuples)
        """

        self.vision = []
        for y_diff in range(-1, 2):
            for x_diff in range(-1, 2):
                cood=(-1,-1)
                if (self.pos[1] + y_diff >= 0 and self.pos[1] + y_diff <= bounds[1] and
                        self.pos[0] + x_diff >= 0 and self.pos[0] + x_diff <= bounds[0]):
                    if x_diff == 0 and y_diff == -1 and maze[self.pos[1] - 1][self.pos[0]] in [' ', 'X']:
                        cood = (self.pos[0], self.pos[1] - 1)
                    elif x_diff == -1 and y_diff == 0 and maze[self.pos[1]][self.pos[0] - 1] in [' ', 'X']:
                        cood = (self.pos[0] - 1, self.pos[1])
                    elif x_diff == 1 and y_diff == 0 and maze[self.pos[1]][self.pos[0] + 1] in [' ', 'X']:
                        cood = (self.pos[0] + 1, self.pos[1])
                    elif x_diff == 0 and y_diff == 1 and maze[self.pos[1] + 1][self.pos[0]] in [' ', 'X']:
                        cood = (self.pos[0], self.pos[1] + 1)

                    if cood not in self.past_cood and cood != (-1, -1):
                        self.vision.append(cood)

        return self.vision

    def solve_maze(self, maze, target, bounds):
        """
        Solves the maze by guiding the agent from the starting position to the target.

        Args:
            maze (list): A 2D list representing the maze.
            target (tuple): The coordinates (x, y) of the exit (target).
            bounds (tuple): A tuple containing the maze dimensions (x_max, y_max).

        Returns:
            bool: True if the maze is solved, False if the maze is unsolvable.
        """

        while self.pos != target and not self.stuck:
            self.vision = self.rewrite_vis(bounds)

            if len(self.vision) == 0:
                if self.crossroads == []:
                    print('Error- Maze Unsolvable')
                    self.stuck = True
                else:
                    self.past_cood.append(self.pos)
                    self.crossroads = self.crossroads + self.vision
                    cood = choose_road(self.crossroads, self.pos, target)
                    self.pos = cood

            elif len(self.vision) == 1:
                self.past_cood.append(self.pos)
                self.pos = self.vision[0]

            elif len(self.vision) > 1:
                self.past_cood.append(self.pos)
                self.crossroads = self.crossroads + self.vision
                cood = choose_road(self.crossroads, self.pos, target)
                self.pos = cood

        if not self.stuck:
            print('Solved Maze: ')
            for cood in self.past_cood:
                maze[int(cood[1])][int(cood[0])] = ","

            for row in maze:
                for cell in row:
                    if cell == "," or cell == "X":
                        print(Fore.RED + cell, end=' ')
                        print(Fore.RESET, end='')
                    else:
                        print(cell, end=' ')
                print('')
            print('')

        return not self.stuck


# Example usage:
filename = 'ENTER MAZE FILE HERE'
maze, target, x_max, y_max, start_x, start_y = create_maze(filename)

agent = Agent()
agent.start = (start_x, start_y)
agent.pos = agent.start

if agent.solve_maze(maze, target, (x_max, y_max)):
    print("Maze solved successfully!")
else:
    print("Maze is unsolvable.")
