import pygame

from settings import *

vec = pygame.math.Vector2


class Player(object):
    def __init__(self, game, pos):
        self.game = game
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        # pacman movement will start going right
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

        self.load()

    def update(self):
        # if no interaction with walls is True
        if self.able_to_move:
            # pacman pix pos change in relation to direction and speed
            self.pix_pos += self.direction * self.speed

        # lock pacman in a grid position when moving
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # update / setting grid position in reference to pixel position for red rect
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_MARGIN + self.game.cell_width // 2) // self.game.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_MARGIN + self.game.cell_height // 2) // self.game.cell_height + 1

        # eating coins
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # drawing the pacman
        pygame.draw.circle(self.game.screen, PLAYER_COLOUR, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.game.cell_width // 2 - 2)

        # drawing the player's lives
        for x in range(self.lives):
            pygame.draw.circle(self.game.screen, PLAYER_COLOUR, (650 + 20 * x, HEIGHT - 50), 7)

        # drawing a red rect to keep track of pacman grid pos movement
        # pygame.draw.rect(self.game.screen, RED, (self.grid_pos[0] * self.game.cell_width + TOP_BOTTOM_MARGIN // 2,
                                                 # self.grid_pos[1] * self.game.cell_height + TOP_BOTTOM_MARGIN // 2
                                                 # , self.game.cell_width, self.game.cell_height), 1)

    # function to blit pacman image
    def blit(self):
        self.game.screen.blit(self.pacman1_right, (int(self.pix_pos.x), int(self.pix_pos.y)))

    # convert pacman's grid pos to pis pos
    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.game.cell_width) + TOP_BOTTOM_MARGIN // 2 + self.game.cell_width // 2
                   , (self.grid_pos[1] * self.game.cell_height) + TOP_BOTTOM_MARGIN // 2 + self.game.cell_height // 2)

    # function store the direction from keyboard to variable stored direction
    def move(self, direction):
        self.stored_direction = direction

    # function check if pacman is moving only if it is in the center of a grid and has a direction
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_MARGIN // 2) % self.game.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_MARGIN // 2) % self.game.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    # function for pacman interaction with wall in wall list
    def can_move(self):
        for wall in self.game.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    # function check if pacman grid pos is on coin grid pos
    def on_coin(self):
        if self.grid_pos in self.game.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_MARGIN // 2) % self.game.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True

            if int(self.pix_pos.y + TOP_BOTTOM_MARGIN // 2) % self.game.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    # function remove coin in list to make coin disappear and add pt in current_score
    def eat_coin(self):
        eat_sound.play()
        self.game.coins.remove(self.grid_pos)
        self.current_score += 1

    # function to load a pacman image and manipulate it
    def load(self):
        self.pacman1_right = pygame.image.load('asset/sprites/84.png').convert_alpha()
        self.pacman1_right = pygame.transform.scale(self.pacman1_right, (self.game.cell_width - 5, self.game.cell_width - 5))
