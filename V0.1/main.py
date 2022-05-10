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


# Definition of colours - Established here for easy and intuitive implementation into later code
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
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
pygame.init()
fpsClock = pygame.time.Clock()

# Sets display window size - Square - number of squares in grid * 15px
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))

# Title of popup window
pygame.display.set_caption('Gluttonous')

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
def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50) # Specifies font and size to use
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
    screen.fill(white) # Background colour


# Main menu - First function called by code
def initial_interface():
    intro = True
    screen.fill(white) # Background colour
    while intro:

        for event in pygame.event.get(): # Alternative for if the application is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() # Modification - Gracefully closes python program if application is closed

        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15) # Title

        button('Play!', 80, 240, 80, 40, green, bright_green, game_loop, 'human') # Calls game_loop function
        button('Quit', 270, 240, 80, 40, red, bright_red, quitgame) # Calls quitgame function

        pygame.display.update() # Refresh screen (Bug - while loop causes flickering of buttons)
        pygame.time.Clock().tick()


# Gameplay Screen
def game_loop(player, fps=10):
    game.restart_game()

    while not game.game_end():

        pygame.event.pump()

        move = human_move() # Receives input from user
        fps = 5 # Determines how often the game is refreshed (speed of snake)
        

        current_segments = list(game.snake.segments)
        game.do_move(move) # Converts raw user input to update snake

        screen.fill(black) # Background colour
        
        # Modification - Snake head no longer disappears when player loses
        if not game.game_end():
            game.snake.blit(rect_len, screen) # Updates snake 

        else:
            # Snake is updated using old position
            game.snake.segments = current_segments
            game.snake.blit(rect_len, screen)
            game.strawberry.blit(screen)
            game.blit_score(white, screen)
            break


        game.strawberry.blit(screen) # Draws/updates food
        game.blit_score(white, screen) # Draws/updates user score

        # Refreshes/updates screen
        pygame.display.flip()
        fpsClock.tick(fps)

    crash() # Triggers crash sequence once game is finished


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
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT)) # Quits game if esc is pressed

    move = game.direction_to_int(direction) # Translates key pressed to int
    return move

# Main function - Entry point into program
if __name__ == "__main__":
    initial_interface() # Loads main menu
