import pygame, random

from settings import *

vec = pygame.math.Vector2


class Enemy(object):
    def __init__(self, game, pos, number):
        self.game = game
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.game.cell_width // 2 - 2)
        # number = index from enemies list
        self.number = number
        self.colour = self.set_colour()
        # initialise ghosts without movement
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        # set a target
        self.target = self.set_target()
        if self.target != self.grid_pos:
            # ghost pix pos change in relation to direction and speed
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                # function to decide on the ghost direction depending on personlaity; random or target direction
                self.move()

        # setting grid position in reference to pixel position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_MARGIN + self.game.cell_width // 2) // self.game.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[
                                1] - TOP_BOTTOM_MARGIN + self.game.cell_height // 2) // self.game.cell_height + 1

    # draw circle for each ghosts
    def draw(self):
        pygame.draw.circle(self.game.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    # convert ghost's grid pos to pis pos
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.game.cell_width) + TOP_BOTTOM_MARGIN // 2 + self.game.cell_width // 2
                   , (self.grid_pos.y * self.game.cell_height) + TOP_BOTTOM_MARGIN // 2 + self.game.cell_height // 2)

    # function return colour depending on the index number
    def set_colour(self):
        if self.number == 0:
            return RED
        if self.number == 1:
            return PINK
        if self.number == 2:
            return ORANGE
        if self.number == 3:
            return LIGHT_BLUE

    # function return personality depending on the index number
    def set_personality(self):
        if self.number == 0:
            return 'speedy'
        elif self.number == 1:
            return 'slow'
        elif self.number == 2:
            return 'random'
        else:
            return 'scared'

    # function to set a target
    def set_target(self):
        # if personality speedy or slow, target the player grid position
        if self.personality == 'speedy' or self.personality == 'slow':
            return self.game.player.grid_pos
        # else i.e scared will target the opposite of player grid position
        else:
            # if player position is bottom right then our target vector must be top left
            if self.game.player.grid_pos[0] > NUM_COLS // 2 and self.game.player.grid_pos[1] > NUM_ROWS // 2:
                return vec(1, 1)
            # if player position is top left then our target vector must be bottom left
            if self.game.player.grid_pos[0] > NUM_COLS // 2 and self.game.player.grid_pos[1] < NUM_ROWS // 2:
                return vec(1, NUM_ROWS-2)
            # if player position is bottom left then our target vector must be top right
            if self.game.player.grid_pos[0] < NUM_COLS // 2 and self.game.player.grid_pos[1] > NUM_ROWS // 2:
                return vec(NUM_COLS-2, 1)
            # if player position is top right then our target vector must be bottom right
            else:
                return vec(NUM_COLS-2, NUM_ROWS-2)

    # function return speed depending on the personality
    def set_speed(self):
        if self.personality in ['speedy', 'scared']:
            speed = 2
        else:
            speed = 1
        return speed

    # function check if ghost is moving only if it is in the center of a grid and has a direction
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_MARGIN // 2) % self.game.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_MARGIN // 2) % self.game.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    # function to decide on the ghost direction depending on personlaity; random or target direction
    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_direction()
        if self.personality == 'slow':
            self.direction = self.get_path_direction(self.target)
        if self.personality == 'speedy':
            self.direction = self.get_path_direction(self.target)
        if self.personality == 'scared':
            self.direction = self.get_path_direction(self.target)

    # function to get a random direction
    def get_random_direction(self):
        while True:
            # generate a random number between 2 and 1
            number = random.randint(-2, 1)
            # depend on random number the direction will change
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            # set next pos of ghost by adding actual position with direction obtained
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            # if next pos is same as a wall pos , break
            if next_pos not in self.game.walls:
                break
        return vec(x_dir, y_dir)

    # function convert the next cell to vector position for direction to move
    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        # target can be player position or for scared opposite direction
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [int(target[0]), int(target[1])])
        # return the next cell
        return path[1]

    # breadth first search function - first in first out
    def BFS(self, start, target):
        # make a grid 29 wide and 30 height full of zero
        grid = [[0 for x in range(28)] for x in range(30)]
        # look though walls to identify the walls
        for cell in self.game.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]  # player position
        path = []
        visited = []
        while queue:
            current = queue[0]
            # remove current from queue
            queue.remove(queue[0])
            # append current to visited
            visited.append(current)
            if current == target:
                break
            else:
                # neighbour: up, down, right, left
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                # this will check if it is a valid direction i.e not colliding with a wall by looping to every direction
                for neighbour in neighbours:
                    # neighbour and current x axis greater than 0; get us to the next cell we want to look at
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        # same but for yaxis
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                # if next cell doesn't collide with a wall, append same to queue list and path
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, 'Next': next_cell})

        # to determine the shortest pos to get to target
        # append shortest list with new target cell
        shortest = [target]
        # while target cell is no same as player pos
        while target != start:
            for step in path:
                # if next cell is equal to target pos
                if step['Next'] == target:
                    target = step['Current']
                    shortest.insert(0, step['Current'])
        return shortest
