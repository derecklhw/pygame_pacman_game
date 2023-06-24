import pygame
from settings import *


class Button(object):
    def __init__(self, game, x, y, width, height, bg_colour, border_colour=RED,
                 hover_colour=None, function=None, text=None):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_colour = bg_colour
        self.border_colour = border_colour
        self.hover_colour = hover_colour
        self.hovered = False
        self.function = function
        self.text = text
        self.font = pygame.font.Font(FONT, BUTTON_TEXT_SIZE)

    # function to determine if the mouse pos collide with the button width and height
    def update(self):
        cursor = pygame.mouse.get_pos()
        if self.x + self.width > cursor[0] > self.x and self.y + self.height > cursor[1] > self.y:
            self.hovered = True
        else:
            self.hovered = False

    # function to draw the button and change it colors when hovered on or not
    def draw(self):
        if not self.hovered:
            pygame.draw.rect(self.game.screen, self.bg_colour, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.game.screen, self.hover_colour, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.game.screen, self.border_colour, (self.x, self.y, self.width, self.height), 2)
        self.show_text()

    # function when button clicked will execute the function variable
    def click(self):
        if self.function != None:
            self.function()
        else:
            pass

    # function to render the text and center its position in the button
    def show_text(self):
        if self.text != None:
            text = self.font.render(self.text, True, BUTTON_TEXT_COLOUR)
            # find the size of the text
            text_size = text.get_size()
            text_x = self.x + (self.width / 2) - (text_size[0] / 2)
            text_y = self.y + (self.height / 2) - (text_size[1] / 2)
            self.game.screen.blit(text, (text_x, text_y))

