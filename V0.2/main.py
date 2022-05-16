# -*- coding: utf-8 -*-
"""
(UPDATE DOCSTRING)
Created on Wed May 16 15:22:20 2018

@author: zou

"""
# Importing necessary modules
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

# Imports Game class defined in 'game.py' which contains Settings, Snake and Strawberry classes
from game import Game

# Modification - Leaderboard
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import config
import random


app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snake.db'
db = SQLAlchemy(app)


# Definition of colours - Established here for easy and intuitive implementation into later code
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
load_green = pygame.Color(100, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

# Initialises Game class (from game.py) and defines settings
game = Game()
rect_len = game.settings.rect_len # Width/height of square icons used during gameplay (in px)
snake = game.snake # Defines snake class within game class for convienence later in the code

# Initialises pygame and sets basic settings

#####Intro#####

def import_and_install(package):
    try:
        return __import__(package)
    except ImportError:
        return None
        
import_and_install('numpy')
import_and_install('pygame')

config.player_name = input("Before playing, please enter your name: ")

pygame.init()
fpsClock = pygame.time.Clock()

font_descript = pygame.font.SysFont("arial", 10, True)
background = pygame.image.load('./logos/gamelogo.png')
team_logo = pygame.image.load('./logos/team.png')

# Sets display window size - Square - number of squares in grid * 15px
# + 25 is the amount of pixels were extended for the score
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15 + 25))

def kick_start(background, progress=0):
    pygame.display.set_caption('Pygame: Loading - Gluttonous')
    font_descript = pygame.font.SysFont("arial", 10, True)
    while (progress/2) < 100:
        time_keep = 0.003
        time_increase = 1
        progress += time_increase
        
        screen.fill(white)
        screen.blit(background, (-80, 10))
        if progress > 100:
            time.sleep(1)
            break
        if (progress/2) > 30:
            pygame.draw.rect(screen, green, [0, 400, 420, 15])
        else:
            pygame.draw.rect(screen, green, [0, 400, progress, 15])
        text = font_descript.render("Loading: " + str(int(progress)) + "%", True, black)
        screen.blit(text, [170, 402.5])
        pygame.display.flip()
        time.sleep(time_keep)


def team_logo_display():
    pygame.display.set_caption('Pygame: Loading - Gluttonous')
    time_kept = 0
    time_keep = 0.03
    screen.fill(white)
    while time_kept < 50:
        time_kept += 1
        screen.blit(team_logo, ((game.settings.width * 15 - team_logo.get_width())/2, (game.settings.height * 15 - team_logo.get_height() - 20)/2))
        pygame.display.flip()
        time.sleep(time_keep)

################


# Modification - Adding application icon
pygame_icon = pygame.image.load('./logos/application.png')
pygame.display.set_icon(pygame_icon)

# Initialising game assets (audio)
crash_sound = pygame.mixer.Sound('./sound/crash.wav')


# Applies required styling to the text given as input
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Used to displays messages on screen in game

def message_display(text, x, y, color=black, size=50):
    large_text = pygame.font.SysFont('comicsansms', size) # Specifies font and size to use
    text_surf, text_rect = text_objects(text, large_text, color) # Links to function above
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect) # Displays text on screen
    pygame.display.update() # Forces program to refresh to show new text


# Used to create buttons that can be pressed in game
def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos() # Gets position of the mouse cursor
    click = pygame.mouse.get_pressed() # Checks if mouse is being clicked
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y: # Checks if mouse is over the button
        pygame.draw.rect(screen, active_color, (x, y, w, h)) # Display button changes colour
        if click[0] == 1 and action != None: # Checks if mouse is clicked
            if parameter != None:
                action(parameter) # Call specified function if it has parameter
            else:
                action() # Call specified function if it does not have a parameter
    else:
        # Display button changes back to original colour
        pygame.draw.rect(screen, inactive_color, (x, y, w, h)) 

    smallText = pygame.font.SysFont('comicsansms', 20) # Defines font for button text
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect) # Updates text on screen


# Quits both pygame and python code - can now be easily called
def quitgame():
    pygame.quit()
    quit()

# Displays the 'crash' screen when required
def crash():
    pygame.mixer.Sound.play(crash_sound) # Plays sound effect
    # Prints game over message on screen
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(1)
    message_display('Game over!', game.settings.width / 2 * 15, game.settings.height / 1.75 * 15, red)
    time.sleep(2)
    
# Modification - Leaderboard
def get_pid():
    return random.randint(1e9, 1e10)

class Model(db.Model):
    pid = db.Column(db.Integer, primary_key=True, default=get_pid)
    player = db.Column(db.String(50))
    score = db.Column(db.Integer)

    def __init__(self, player, score):
        self.player = player
        self.score = score


# Displays the 'crash' screen when required
def crash():
    pygame.mixer.Sound.play(crash_sound) # Plays sound effect
    high_score = db.session.query(func.max(Model.score)).scalar()
    
    current_game = Model(config.player_name, game.snake.score)
    db.session.add(current_game)
    db.session.commit()
    
    pygame.mixer.music.stop()
    
    # Prints game over message on screen
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(1)
    if config.has_potion:
        config.has_potion = 0
        config.new_life = 1
        message_display('Potion Used', game.settings.width / 2 * 15, game.settings.height / 1.75 * 15, green)
        time.sleep(2)
        game_loop('human')

    elif game.snake.score > high_score:
        message_display('NEW HIGHSCORE!', game.settings.width / 2 * 15, game.settings.height / 1.75 * 15, green)
        time.sleep(2)
    else:   
        message_display('Game over!', game.settings.width / 2 * 15, game.settings.height / 1.75 * 15, red)
        time.sleep(2)
        
    screen.fill(white)
    # loads and prints background of the main page
    bg_img = pygame.image.load("logos/gamelogo.png")
    screen.blit(bg_img, (0,0))

# Main menu - First function called by code
def initial_interface():
    # Title of popup window
    pygame.display.set_caption('Gluttonous')
    
    config.new_life = 0
    intro = True
    screen.fill(white) # Background colour
    
    # loads and prints background of the main page
    bg_img = pygame.image.load("logos/gamelogo.png")
    screen.blit(bg_img, (0,0))
        
    while intro:
        # Application is closed
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                # Modification - Gracefully closes python program
                quit() 

        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15) # Title
        
        high_score = db.session.query(func.max(Model.score)).scalar()
        message_display('Highscore: ' + str(high_score), game.settings.width/2*15, \
                        game.settings.height /2.5*15, size=28)

        button('Play!', 80, 240, 80, 40, green, bright_green, game_loop, 'human') # Calls game_loop function
        button('Quit', 270, 240, 80, 40, red, bright_red, quitgame) # Calls quitgame function

        pygame.display.update() # Refresh screen (Bug - while loop causes flickering of buttons)
        pygame.time.Clock().tick()


# Gameplay Screen
def game_loop(player, fps=10):
    game.restart_game()
    
    bg_img2 = pygame.image.load("images/background.png") # loads board background

    if config.new_life:
        config.new_life = 0

    pos_x = game.settings.width*15/2 - 45
    high_score = db.session.query(func.max(Model.score)).scalar()
    config.fps = fps
    config.game_over = 0

    # print(game.snake.segments) debug
    
    pygame.mixer.music.load('sound/background_music.mp3') # loads the music
    pygame.mixer.music.play(-1) # plays the music on repeat

    while not game.game_end() and not config.game_over:
        pygame.event.pump()

        move = human_move() # Receives input from user
        fps = config.fps # Determines how often the game is refreshed (speed of snake)
        
        current_segments = list(game.snake.segments)
        game.do_move(move, screen) # Converts raw user input to update snake

        screen.blit(bg_img2, (0, 25)) # prints the new background in each draw call
        
        
        # Modification - Snake head no longer disappears when player loses
        if not game.game_end():
            game.snake.blit(rect_len, screen) # Updates snake 

        else:
            # Snake is updated using old position
            config.game_over = 1
            game.snake.segments = current_segments
            game.snake.blit(rect_len, screen)
        
        game.strawberry.blit(screen) # Draws/updates food
        
        if config.mushroom_out:
            game.mushroom.blit(screen)

        if config.super_fruit_out:
            game.super_fruit.blit(screen)
        
        if config.potion_out:
            game.potion.blit(screen)


        game.blit_score(white, screen) # Draws/updates user score
        speed_message = 'Speed: ' + str(config.fps)
        small_message(white, screen, speed_message, game.settings.width*15-85, 5)        
        if game.snake.score > high_score:
            message = 'Highscore: ' + str(game.snake.score)
            small_message(white, screen, message, pos_x, 5)
        else:    
            message = 'Highscore: ' + str(high_score)
            small_message(white, screen, message, pos_x, 5)

        # Refreshes/updates screen
        pygame.display.flip()
        fpsClock.tick(fps)

    crash() # Triggers crash sequence once game is finished
    
def small_message(color, screen, message, pos_x, pos_y):
    font = pygame.font.SysFont(None, 25)
    text_surf, text_rect = text_objects(message, font, color)
    text_rect.center = (pos_x, pos_y)
    screen.blit(text_surf, (pos_x, pos_y)) # make sure this works


# Reads user input
def human_move():
    direction = snake.facing # Previous direction received from user

    for event in pygame.event.get(): # Quits the program if the application is closed
        if event.type == QUIT:
            pygame.quit()
            quit()

        elif event.type == KEYDOWN: # User presses a key to change the snake's direction
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE or event.key == ord('q'):
                pygame.event.post(pygame.event.Event(QUIT)) # Quits game if esc is pressed

    move = game.direction_to_int(direction) # Translates key pressed to int
    return move

# Main function - Entry point into program
if __name__ == "__main__":
    kick_start(background) # loading screen
    team_logo_display() # loads logo
    initial_interface() # Loads main menu
