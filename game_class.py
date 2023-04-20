import pygame, sys, threading
import time

from settings import *
from player_class import *
from enemy_class import *
from button_class import *

pygame.init()
# assign Vector 2 function to vec variable
vec = pygame.math.Vector2


class Game(object):
    def __init__(self):
        # general setup of pygame library
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("pacman.exe")
        # clock to control the frame per sec
        self.clock = pygame.time.Clock()

        # load and play theme music
        pygame.mixer.music.load('asset/music/Theme_Game.wav')
        pygame.mixer.music.play(loops=-1)

        self.running = True
        self.paused = False
        self.display_score = False
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // NUM_COLS
        self.cell_height = MAZE_HEIGHT // NUM_ROWS
        self.intro_buttons = []
        self.playing_buttons = []
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemy_pos = []
        self.scores = []
        self.player_pos = None
        self.load()
        self.player = Player(self, vec(self.player_pos))
        self.make_enemies()
        self.make_buttons()
        self.get_score()

        # game-over blink text
        self.col_spd = 1    # increment and decrement
        self.col_dir = [1, 1, 1]  # increment and decrement direction
        self.minimum = 0
        self.maximum = 255
        self.color_list = [[120, 120, 240], [120, 120, 240], [120, 120, 240], [120, 120, 240], [120, 120, 240],
                           [120, 120, 240], [120, 120, 240], [120, 120, 240], [120, 120, 240]]

    # the game will have 3 main states; start, playing and game_over
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game_over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ################################################  GENERAL FUNCTIONS ###############################################

    # function to draw text on the screen
    def draw_text(self, screen, text, font_name, font_size, colour, pos, centered=False):
        text_font = pygame.font.Font(font_name, font_size)
        text_surf = text_font.render(text, False, colour)
        if centered:
            text_rect = text_surf.get_rect(center=pos)
        else:
            text_rect = text_surf.get_rect(topleft=pos)
        screen.blit(text_surf, text_rect)

    # function to create the button and append them to a list respective to the game state
    def make_buttons(self):
        # intro_buttons
        intro_play_button = Button(self, (WIDTH // 2) // 2 - 100, HEIGHT // 2, 150, 50, ORANGE,
                                   hover_colour=LIGHT_ORANGE, function=self.intro_to_play, text="PLAY")
        self.intro_buttons.append(intro_play_button)

        intro_view_score_button = Button(self, (WIDTH // 2) - 110, HEIGHT // 2, 230, 50, GREY, hover_colour=LIGHT_GREY,
                                         function=self.score, text="VIEW SCORES")
        self.intro_buttons.append(intro_view_score_button)

        intro_quit_button = Button(self, (WIDTH // 2) + 150, HEIGHT // 2, 150, 50, RED, hover_colour=LIGHT_RED,
                                   function=self.intro_to_quit, text="QUIT")
        self.intro_buttons.append(intro_quit_button)

        # playing buttons
        playing_pause_button = Button(self, 590, HEIGHT // 2 - 100, 150, 50, ORANGE, hover_colour=LIGHT_ORANGE,
                                      function=self.pause, text="PAUSE")
        self.playing_buttons.append(playing_pause_button)
        playing_quit_button = Button(self, 590, HEIGHT // 2, 150, 50, RED, hover_colour=LIGHT_RED,
                                     function=self.intro_to_quit, text="QUIT")
        self.playing_buttons.append(playing_quit_button)

    # function where we will load png and do file handling before running our game
    def load(self):
        # start screen
        # pacman_banner image loading and manipulation
        self.pacman_banner = pygame.image.load('asset/sprites/0.png').convert_alpha()
        self.pacman_banner_scaled = pygame.transform.rotozoom(self.pacman_banner, 0, 2)
        self.pacman_banner_rect = self.pacman_banner_scaled.get_rect(center=(WIDTH // 2, 150))

        # multiple pacman images loading in a list for animation
        self.pacman_left_1 = pygame.image.load('asset/sprites/13.png').convert_alpha()
        self.pacman_left_1 = pygame.transform.rotozoom(self.pacman_left_1, 0, 3)
        self.pacman_left_2 = pygame.image.load('asset/sprites/14.png').convert_alpha()
        self.pacman_left_2 = pygame.transform.rotozoom(self.pacman_left_2, 0, 3)
        self.pacman_left = [self.pacman_left_1, self.pacman_left_2]
        # switch between 2 images every few millisecond
        self.pacman_left_index = 0
        self.pacman_left_surf = self.pacman_left[self.pacman_left_index]
        self.pacman_left_rect = self.pacman_left_surf.get_rect(midtop=(WIDTH, HEIGHT - 50))

        # multiple red ghost images loading in a list for animation
        self.red_ghost_1 = pygame.image.load('asset/sprites/39.png').convert_alpha()
        self.red_ghost_1 = pygame.transform.rotozoom(self.red_ghost_1, 0, 3)
        self.red_ghost_2 = pygame.image.load('asset/sprites/40.png').convert_alpha()
        self.red_ghost_2 = pygame.transform.rotozoom(self.red_ghost_2, 0, 3)
        self.red_ghost = [self.red_ghost_1, self.red_ghost_2]
        self.red_ghost_index = 0
        self.red_ghost_surf = self.red_ghost[self.red_ghost_index]
        self.red_ghost_rect = self.red_ghost_surf.get_rect(midtop=(WIDTH + 100, HEIGHT - 50))

        # multiple orange ghost images loading in a list for animation
        self.orange_ghost_1 = pygame.image.load('asset/sprites/65.png').convert_alpha()
        self.orange_ghost_1 = pygame.transform.rotozoom(self.orange_ghost_1, 0, 3)
        self.orange_ghost_2 = pygame.image.load('asset/sprites/66.png').convert_alpha()
        self.orange_ghost_2 = pygame.transform.rotozoom(self.orange_ghost_2, 0, 3)
        self.orange_ghost = [self.orange_ghost_1, self.orange_ghost_2]
        self.orange_ghost_index = 0
        self.orange_ghost_surf = self.orange_ghost[self.orange_ghost_index]
        self.orange_ghost_rect = self.orange_ghost_surf.get_rect(midtop=(WIDTH + 150, HEIGHT - 50))

        # playing screen
        # background maze image loading and manipulation
        self.background = pygame.image.load('asset/sprites/maze.png').convert()
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # opening wall.txt and read data from it
        with open('walls.txt', 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    # appending walls list with coordinate of walls
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))
                    # appending coins list with coordinate of walls
                    elif char == 'C':
                        self.coins.append(vec(xidx, yidx))
                    # obtain player_pos
                    elif char == 'P':
                        self.player_pos = [xidx, yidx]
                    # obtain ghosts_pos and append in enemy pos list
                    elif char in ["2", "3", "4", "5"]:
                        self.enemy_pos.append(vec(xidx, yidx))
                    # draw black rectangle for entrance of ghost home
                    elif char in 'B':
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))

        # print(self.walls)

    # function draw a grid on the background image for walls position and pacman movement
    def draw_grid(self):
        # draw grid in x-axis
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        # draw grid in y-axis
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height), (WIDTH, x * self.cell_height))
        # draw a blue rectangle for the walls from walls list
        for wall in self.walls:
            pygame.draw.rect(self.background, BLUE,
                             (wall.x * self.cell_width, wall.y * self.cell_height, self.cell_width, self.cell_height))

    ################################################  START FUNCTIONS #################################################

    def start_events(self):
        # access a list of Pygame keeps for all the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # self.state = 'playing'

            # if user hover on an intro buttons and mouse click on it, execute button.click function
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.intro_buttons:
                    if button.hovered:
                        button.click()

    def start_update(self):
        for button in self.intro_buttons:
            button.update()

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, '1UP', FONT, START_FONT_SIZE, RED, (2, 2))
        self.draw_text(self.screen, 'HI-SCORE', FONT, START_FONT_SIZE, RED, (WIDTH // 2, 12), centered=True)
        self.draw_text(self.screen, 'V-1.4', FONT, START_FONT_SIZE, RED, (WIDTH - 110, 2))
        self.draw_text(self.screen, '00', FONT, START_FONT_SIZE, WHITE, (60, 27))
        self.draw_text(self.screen, f'{self.scores[0]}', FONT, START_FONT_SIZE, WHITE, ((WIDTH // 2) + 44, 37),
                       centered=True)

        # self.draw_text(self.screen, 'PUSH SPACE BAR', START_FONT, START_FONT_SIZE, PALE_CANARY,
        #                (WIDTH // 2, HEIGHT // 2), centered=True)

        for button in self.intro_buttons:
            button.draw()

        self.draw_text(self.screen, '1 PLAYER ONLY', FONT, START_FONT_SIZE, LIGHT_BLUE,
                       (WIDTH // 2, (HEIGHT // 2) + 125), centered=True)
        self.draw_text(self.screen, '© 1980, 1984 NAMCO LTD.', FONT, START_FONT_SIZE, WHITE,
                       (WIDTH // 2, (HEIGHT // 2) + 175), centered=True)
        self.draw_text(self.screen, 'LICENCED TO NINTENDO', FONT, START_FONT_SIZE, WHITE,
                       (WIDTH // 2, (HEIGHT // 2) + 225), centered=True)
        self.screen.blit(self.pacman_banner_scaled, self.pacman_banner_rect)

        # basic animation for pacman and ghosts
        # pacman movement direction will be to the left
        self.pacman_left_rect.x -= 3
        # if pacman reach the end of the screen, change its screen pos
        if self.pacman_left_rect.right <= 0:
            self.pacman_left_rect.left = WIDTH + 20
        # pacman image switch function
        self.pacman_animation()
        self.screen.blit(self.pacman_left_surf, self.pacman_left_rect)

        # red ghost movement direction
        self.red_ghost_rect.x -= 3
        if self.red_ghost_rect.right <= 0:
            self.red_ghost_rect.left = WIDTH + 20
        self.red_ghost_animation()
        self.screen.blit(self.red_ghost_surf, self.red_ghost_rect)

        # orange ghost movement direction
        self.orange_ghost_rect.x -= 3
        if self.orange_ghost_rect.right <= 0:
            self.orange_ghost_rect.left = WIDTH + 20
        self.orange_ghost_animation()
        self.screen.blit(self.orange_ghost_surf, self.orange_ghost_rect)

        pygame.display.update()

    # image switching animation for pacman and ghost
    def pacman_animation(self):
        # change the index at a slow speed
        self.pacman_left_index += 0.1
        # a loop where when index is greater than length of image list, reinitialize the index to zero
        if self.pacman_left_index >= len(self.pacman_left):
            self.pacman_left_index = 0
        # change the surface variable image as per the image index
        self.pacman_left_surf = self.pacman_left[int(self.pacman_left_index)]

    def red_ghost_animation(self):
        self.red_ghost_index += 0.1
        if self.red_ghost_index >= len(self.red_ghost):
            self.red_ghost_index = 0
        self.red_ghost_surf = self.red_ghost[int(self.red_ghost_index)]

    def orange_ghost_animation(self):
        self.orange_ghost_index += 0.1
        if self.orange_ghost_index >= len(self.orange_ghost):
            self.orange_ghost_index = 0
        self.orange_ghost_surf = self.orange_ghost[int(self.orange_ghost_index)]

    def intro_to_play(self):
        self.state = 'playing'

    def intro_to_quit(self):
        self.running = False

    ################################################  PLAYING FUNCTIONS ################################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # pacman movement in relation to keyboard keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

                # if event.key == pygame.K_p:
                # self.pause()

            # if user hover on an intro buttons and mouse click on it, execute button.click function
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.playing_buttons:
                    if button.hovered:
                        button.click()

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        # for loop, if enemy grid pos is on player grid pos
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

        for button in self.playing_buttons:
            button.update()

    def playing_draw(self):
        # stop theme music
        pygame.mixer.music.stop()
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_MARGIN // 2, TOP_BOTTOM_MARGIN // 2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text(self.screen, 'HI-SCORE', FONT, PLAYING_FONT_SIZE, RED, (600, 32))
        # draw the high score
        self.draw_text(self.screen, f'{self.scores[0]}', FONT, PLAYING_FONT_SIZE, WHITE, (650, 52))
        self.draw_text(self.screen, '1UP', FONT, PLAYING_FONT_SIZE, RED, (620, 102))
        # draw the current score
        self.draw_text(self.screen, f'{self.player.current_score}', FONT, PLAYING_FONT_SIZE, WHITE, (650, 122))
        self.draw_text(self.screen, 'LIVES', FONT, PLAYING_FONT_SIZE, RED, (600, HEIGHT - 90))
        # draw playing buttons
        for button in self.playing_buttons:
            button.draw()
        # self.player.blit()
        self.player.draw()
        # draw each ghosts from enemy lists
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    # function draw circle for coins in coin list
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, PALE_CANARY,
                               (int(coin.x * self.cell_width) + TOP_BOTTOM_MARGIN // 2 + self.cell_width // 2,
                                int(coin.y * self.cell_height) + TOP_BOTTOM_MARGIN // 2 + self.cell_height // 2), 5)

    # function to create each enemies from enemy pos list
    def make_enemies(self):
        for idx, pos in enumerate(self.enemy_pos):
            # create a class object for each ghost with an index and pos to append in enemies list
            self.enemies.append(Enemy(self, pos, idx))

    def remove_life(self):
        death_sound.play()
        time.sleep(2)
        self.player.lives -= 1
        # if lives is zero, gameover state
        if self.player.lives == 0:
            # execute function to check if current score is a new high score
            self.check_scores()
            self.state = 'game_over'
        else:
            # set player to starting pos
            self.player.grid_pos = vec(self.player.starting_pos)
            # set pix pos variable in player class to conversion of starting grid pos
            self.player.pix_pos = self.player.get_pix_pos()
            # set direction movement is equal to zero
            self.player.direction *= 0
            # set all ghosts to starting pos
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                # set pix pos variable in enemies class to conversion of starting grid pos
                enemy.pix_pos = enemy.get_pix_pos()
                # set direction movement is equal to zero
                enemy.direction *= 0

    ################################################ GAME OVER FUNCTIONS ###############################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # press on key space to reset the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            # press on key esc to exit the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    # blinking function
    def col_change(self, color, dir):
        for i in range(3):
            # increment each rgb value
            color[i] += self.col_spd * dir[i]
            if color[i] >= self.maximum or color[i] <= self.minimum:
                dir[i] *= -1

    def game_over_draw(self):
        self.screen.fill(BLACK)

        # self.draw_text(self.screen, 'GAME OVER', FONT, START_FONT_SIZE, RED,
        #               (WIDTH // 2, HEIGHT // 2), centered=True)

        # draw the letter of the Gameover word separately and assign them to a colour
        self.draw_text(self.screen, "G", FONT, GAME_OVER_FONT_SIZE, self.color_list[0],
                       (int(WIDTH * 0.33), HEIGHT // 2), centered=True)
        self.draw_text(self.screen, "A", FONT, GAME_OVER_FONT_SIZE, self.color_list[1],
                       (int(WIDTH * 0.33) + 40, HEIGHT // 2), centered=True)
        self.draw_text(self.screen, "M", FONT, GAME_OVER_FONT_SIZE, self.color_list[2],
                       (int(WIDTH * 0.33) + 80, HEIGHT // 2), centered=True)
        self.draw_text(self.screen, "E", FONT, GAME_OVER_FONT_SIZE, self.color_list[3],
                       (int(WIDTH * 0.33) + 120, HEIGHT // 2), centered=True)
        self.draw_text(self.screen, "O", FONT, GAME_OVER_FONT_SIZE, self.color_list[4],
                       (int(WIDTH * 0.33) + 160, HEIGHT // 2), centered=True)
        self.draw_text(self.screen, "V", FONT, GAME_OVER_FONT_SIZE, self.color_list[5],
                       (int(WIDTH * 0.33) + 200, HEIGHT // 2), centered=True)
        self.draw_text(self.screen, "E", FONT, GAME_OVER_FONT_SIZE, self.color_list[6],
                       (int(WIDTH * 0.33) + 240, HEIGHT // 2), centered=True)
        self.draw_text(self.screen, "R", FONT, GAME_OVER_FONT_SIZE, self.color_list[7],
                       (int(WIDTH * 0.33) + 280, HEIGHT // 2), centered=True)

        # thread each blinking text
        blink_one = threading.Thread(target=self.col_change, args=(self.color_list[0], self.col_dir)).start()
        blink_two = threading.Thread(target=self.col_change, args=(self.color_list[1], self.col_dir)).start()
        blink_three = threading.Thread(target=self.col_change, args=(self.color_list[2], self.col_dir)).start()
        blink_four = threading.Thread(target=self.col_change, args=(self.color_list[3], self.col_dir)).start()
        blink_five = threading.Thread(target=self.col_change, args=(self.color_list[4], self.col_dir)).start()
        blink_six = threading.Thread(target=self.col_change, args=(self.color_list[5], self.col_dir)).start()
        blink_seven = threading.Thread(target=self.col_change, args=(self.color_list[6], self.col_dir)).start()
        blink_eight = threading.Thread(target=self.col_change, args=(self.color_list[7], self.col_dir)).start()

        # draw text for retry and exit
        self.draw_text(self.screen, 'PRESS SPACEBAR - TO RETRY', FONT, START_FONT_SIZE, RED,
                       (WIDTH // 2, (HEIGHT // 2 + 80)), centered=True)
        self.draw_text(self.screen, 'PRESS ESC KEY - TO EXIT', FONT, START_FONT_SIZE, RED,
                       (WIDTH // 2, (HEIGHT // 2 + 160)), centered=True)

        pygame.display.update()

    def reset(self):
        # reset lives, current score and sprites starting pos
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.grid_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        # reset the coins list and append the vector position of the coins in the list
        self.coins = []
        with open('walls.txt', 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = 'playing'

    ################################################ PAUSE FUNCTIONS ###################################################

    # function will be executed when pause button clicked
    def pause(self):
        # play pause sound
        pause_sound.play()
        self.paused = True
        # when pause, go through the event loop, to see what the user is doing
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # press key C to continue the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    self.paused = False

            # fill the screen to black and draw some texts
            self.screen.fill(BLACK)
            self.draw_text(self.screen, 'PAUSE', FONT, START_FONT_SIZE, RED,
                           (WIDTH // 2, HEIGHT // 2), centered=True)
            self.draw_text(self.screen, 'PRESS C - TO CONTINUE', FONT, START_FONT_SIZE, RED,
                           (WIDTH // 2, HEIGHT // 2 + 50), centered=True)

            # pacman and ghost animation and position on screen
            self.pacman_animation()
            self.screen.blit(self.pacman_left_surf, (WIDTH // 2 + 100, HEIGHT - 200))
            self.red_ghost_animation()
            self.screen.blit(self.red_ghost_surf, (WIDTH // 2, HEIGHT - 200))
            self.orange_ghost_animation()
            self.screen.blit(self.orange_ghost_surf, (WIDTH // 2 - 50, HEIGHT - 200))

            pygame.display.update()
            self.clock.tick(30)

    ################################################ HIGH SCORES FUNCTIONS ##################################################

    # run on initialization of start screen
    def get_score(self):
        with open("scores.txt", 'r') as file:
            for line in file:
                self.scores.append(line.strip())

            # convert item in txt file from str to int
            for idx, score in enumerate(self.scores):
                self.scores[idx] = int(self.scores[idx])

            # print(self.scores)

    # function executed when game over
    def check_scores(self):
        # loop through the scores list initialize
        for score in self.scores:
            if self.player.current_score > score:
                self.new_highscore()
                return True

    def new_highscore(self):
        # append the new high score to the list and sort the list
        self.scores.append(self.player.current_score)
        self.scores.sort(reverse=True)
        print(self.scores)
        # keep only a list of 5 integers
        self.scores = self.scores[0:5]
        self.set_scores()

    def set_scores(self):
        # amend text file with new high scores
        with open('scores.txt', 'w') as file:
            for score in self.scores:
                file.write(str(score) + '\n')

    # function will be executed when view score button clicked
    def score(self):
        self.display_score = True
        while self.display_score:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # press key M to return to start screen
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.display_score = False

            # fill the screen to black and draw the high score table
            self.screen.fill(BLACK)
            self.draw_text(self.screen, "SCORES", FONT, 30, WHITE, (WIDTH // 2, 40), centered=True)
            y = 80
            for rank, score in enumerate(self.scores):
                y += 50
                rank += 1
                self.draw_text(self.screen, f'{rank}th\t\t\t{score}', FONT, START_FONT_SIZE, WHITE,
                               (WIDTH // 2 - 80, y))
            self.draw_text(self.screen, 'PRESS M - FOR MAIN SCREEN', FONT, START_FONT_SIZE, RED,
                           ((WIDTH // 2) + 30, HEIGHT // 2 + 50), centered=True)
            pygame.display.update()
            self.clock.tick(5)
