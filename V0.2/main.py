# Importing necessary modules
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT
import webbrowser

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
green_dark = pygame.Color(0, 100, 0)
bright_green = pygame.Color(0, 255, 0)
load_green = pygame.Color(100, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)
grey = pygame.Color(194, 197, 204)


# Modification - Addition of new buttons and designs
go_button = pygame.image.load('./logos/go_button.png')
go_button_highlight = pygame.image.load('./logos/go_button_highlighted.png')

quit_button = pygame.image.load('./logos/quit_button.png')
quit_button_highlighted = pygame.image.load('./logos/quit_button_highlighted.png')

high_button = pygame.image.load('./logos/hi-score.png')
high_button_highlighted = pygame.image.load('./logos/hi-score_highlighted.png')

help_button = pygame.image.load('./logos/help.png')
help_button_highlighted = pygame.image.load('./logos/help_highlighted.png')

back_button = pygame.image.load('./logos/back.png')
back_button_highlighted = pygame.image.load('./logos/back_highlighted.png')

background = pygame.image.load('./logos/loading_1_1.png')
team_logo = pygame.image.load('./logos/loading_2.png')
bg_img2 = pygame.image.load('images/background.png')

font_descript = pygame.font.SysFont("arial", 10, True)

# Initialises Game class (from game.py) and defines settings
game = Game()
rect_len = game.settings.rect_len # Width/height of square icons used during gameplay (in px)
snake = game.snake # Defines snake class within game class for convienence later in the code


# Modification - Installs required packages during loading screen 
def import_and_install(package):
    try:
        return __import__(package)
    except ImportError:
        return None

# Installing the neccessary packages
import_and_install('numpy')
import_and_install('pygame')
import_and_install('config')

# Modification - Addition of player name for leaderboard
config.player_name = input("Before playing, please enter your name: ")

# Initalises game with required inputs
pygame.init()
fpsClock = pygame.time.Clock()



# Sets display window size
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15 + 25))


# Modification - Loading Screen
def kick_start(background, progress=0):
    current_game = Model(config.player_name, 0)
    db.session.add(current_game)
    db.session.commit()
    
    pygame.display.set_caption('Pygame: Loading - Gluttonous')
    font_descript = pygame.font.SysFont("arial", 10, True)
    while (progress/2) < 100:
        time_keep = 0.003
        time_increase = 1
        progress += time_increase
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                quitgame()

        screen.fill(white)
        screen.blit(background, (0, 0))
        
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


# Displays team logo after loading screen
def team_logo_display():
    pygame.display.set_caption('Pygame: Loading - Gluttonous')
    time_kept = 0
    time_keep = 0.03
    screen.fill(white)
    while time_kept < 50:
        time_kept += 1
        screen.blit(team_logo, (0,0))
        pygame.display.flip()
        time.sleep(time_keep)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                quitgame()


# Modification - Adding application icon
pygame_icon = pygame.image.load('./logos/application.png')
pygame.display.set_icon(pygame_icon)

# Initialising game assets (audio)
crash_sound = pygame.mixer.Sound('./sound/crash.wav')
game_over = pygame.mixer.Sound('./sound/game_over.mp3')
drinking_potion = pygame.mixer.Sound('./sound/drinking_potion.mp3')
high = pygame.mixer.Sound('./sound/highscore.mp3')

# Applies required styling to the text given as input
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Used to displays messages on screen in game - Modified so it can use different size/colour
def message_display(text, x, y, color=black, size=50):
    large_text = pygame.font.SysFont('comicsansms', size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


# Used to create buttons that can be pressed in game
def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos() # Gets position of the mouse cursor
    click = pygame.mouse.get_pressed() # Checks if mouse is being clicked
   
    # Checks if mouse is over the button
    if x + w > mouse[0] > x and y + h > mouse[1] > y: 
    
        # based on the msg, assigns it an image
        if (msg == 'Play!'):
            screen.blit(go_button_highlight, (x, y))
        
        elif (msg == 'Quit'):
            screen.blit(quit_button_highlighted, (x, y))
        
        elif (msg == 'Help'):
            screen.blit(help_button_highlighted, (x,y))
            
        elif (msg == 'Highscores'):
            screen.blit(high_button_highlighted, (x,y))
            
        elif (msg == 'BACK'):
            screen.blit(back_button_highlighted, (x,y))
            
        else:
            # Fallback (original) button if images cannot load
            pygame.draw.rect(screen, active_color, (x, y, w, h)) # Display button changes colour
        
        # Checks if mouse is clicked
        if click[0] == 1 and action != None: 
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        if (msg == 'Play!'):
            screen.blit(go_button, (x, y))
        
        elif (msg == 'Quit'):
            screen.blit(quit_button, (x, y))
            
        elif (msg == 'Help'):
            screen.blit(help_button, (x,y))
            
        elif (msg == 'Highscores'):
            screen.blit(high_button, (x,y))
            
        elif (msg == 'BACK'):
            screen.blit(back_button, (x,y))
            
        else:
            # Fallback (original) button if images cannot load
            pygame.draw.rect(screen, inactive_color, (x, y, w, h))
            smallText = pygame.font.SysFont('comicsansms', 20) # Defines font for button text
            TextSurf, TextRect = text_objects(msg, smallText)
            TextRect.center = (x + (w / 2), y + (h / 2))
            screen.blit(TextSurf, TextRect) # Updates text on screen


# Quits both pygame and python code - can now be easily called
def quitgame():
    pygame.quit()
    quit()

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
    
    pygame.mixer.music.stop() # Stops sound effect
    
    high_score = db.session.query(func.max(Model.score)).scalar() # Gathers new highscore
    
    current_game = Model(config.player_name, game.snake.score)
    db.session.add(current_game)
    db.session.commit()

    # Prints game over message on screen
    message_display('Crashed!', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    
    time.sleep(1)
    if config.has_potion:
        config.has_potion = 0
        config.new_life = 1
        message_display('Potion Used', game.settings.width / 2 * 15, game.settings.height / 1.75 * 15, green_dark)
        
        pygame.mixer.Sound.play(drinking_potion)
        time.sleep(2)
        game_loop('human')

    elif game.snake.score > high_score:
        message_display('NEW HIGHSCORE!', game.settings.width / 2 * 15, game.settings.height / 1.75 * 15, green_dark, 40)
        
        pygame.mixer.Sound.play(high)
        
        time.sleep(2)
    else:   
        message_display('Game over!', game.settings.width / 2 * 15, game.settings.height / 1.75 * 15, red)
        
        pygame.mixer.Sound.play(game_over)
        time.sleep(2)
        
    # creates new background for main page
    bg_img = pygame.image.load('images/background.png')
    screen.blit(bg_img, (0,0))
    
    # loads title for main page
    title = pygame.image.load("logos/title.png")
    screen.blit(title, (25, 50))
    pygame.mixer.music.play(-1)

# Main menu - First function called by code
def initial_interface():
    # Title of popup window
    pygame.display.set_caption('Gluttonous')
    
    config.new_life = 0
    intro = True
    
    # creates new background for main page
    bg_img = pygame.image.load('images/background.png')
    screen.blit(bg_img, (0,0))
    
    # loads title for main page
    title = pygame.image.load("logos/title.png")
    screen.blit(title, (25, 50))
    

    while intro:
        # Application is closed
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                quitgame()
        
        # Modification - Shows highscore and welcomes user on home screen
        high_score = db.session.query(func.max(Model.score)).scalar() # Gets highest score
        message_display('Highscore: ' + str(high_score), game.settings.width/2*15, \
                        game.settings.height /2.5*15, size=28) # Displays highscore
        message_display('Welcome ' + str(config.player_name) + '!', game.settings.width/2*15, \
                        game.settings.height /3.15*15, size=28) # Displays player's name
       
        
        # Modification - New buttons
        button('Play!', 80, 240, 80, 40, green, bright_green, game_loop, 'human') # Plays game
        button('Quit', 270, 240, 80, 40, red, bright_red, quitgame) # Quits the game
        button('Help', 270, 300, 80, 40, blue, bright_blue, help_page) # Page link to manual

        if db.session.query(func.max(Model.score)).scalar() > 0:
            button('Highscores', 80, 300, 80, 40, green, bright_green, view_hs) # Leaderboard
        else:
            button('Highscores', 80, 300, 80, 40, grey, grey)

        pygame.display.update()
        pygame.time.Clock().tick()


# Modification - Leaderboard screen
def view_hs():
    pygame.display.set_caption('Gluttonous: High Score') # Title bar description
    about = True
    
    # creates new background for main page
    bg_img = pygame.image.load('images/background.png')
    screen.blit(bg_img, (0,0))
    
    while about:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                quitgame()
                
        button('BACK', 10, 10, 80, 40, blue, bright_blue, initial_interface)
        pygame.display.update()
        pygame.time.Clock().tick()


# Modification - Help page with link to manual
def help_page():
    pygame.display.set_caption('Gluttonous: Help') # Title bar description
    
    # creates new background for main page
    bg_img = pygame.image.load('images/background.png')
    screen.blit(bg_img, (0,0))
    
    link_font = pygame.font.SysFont('arial', 20)
    link_colour = (0, 0, 0)
    
    while True:
        button('BACK', 10, 10, 80, 40, blue, bright_blue, initial_interface) # Back button -> Main menu 
        screen.blit(link_font.render("Please refer to the Game Manual.", True, black), (60, 60))
        
        # Text button -> Weblink
        game_man = screen.blit(link_font.render("-->>GAME MANUAL<<--", True, link_colour), (100, 100)) 
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                quitgame()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if game_man.collidepoint(pos):
                    webbrowser.open("https://unisydneyedu-my.sharepoint.com/:w:/g/personal/papi6478" \
                            + "_uni_sydney_edu_au/Eb1_y4EqwrdMrb87UmkyY6ABGm8KpPnAQbew_4DYnWHVTQ?e=KHhSGB")
            
        if game_man.collidepoint(pygame.mouse.get_pos()):
            link_colour = (70, 29, 219)
        else:
            link_colour = (0, 0, 0)
        
        pygame.display.update()
        pygame.time.Clock().tick()    


# Gameplay Screen
def game_loop(player, fps=10):
    game.restart_game()
    if config.new_life:
        config.new_life = 0

    pos_x = game.settings.width*15/2 - 45
    high_score = db.session.query(func.max(Model.score)).scalar()
    config.fps = fps
    config.game_over = 0
    
    pygame.mixer.music.play(-1)
    
    while not game.game_end() and not config.game_over:
        pygame.event.pump()

        move = human_move() # Receives input from user
        fps = config.fps # Determines how often the game is refreshed (speed of snake)
        

        current_segments = list(game.snake.segments)
        game.do_move(move, screen) # Converts raw user input to update snake
        
        screen.fill(black)
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
        # Modification - Show potion on scoreboard after consuming
        elif config.has_potion:
            screen.blit(game.potion.image, (85,5))



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
    screen.blit(text_surf, (pos_x, pos_y))


# Reads user input
def human_move():
    direction = snake.facing # Previous direction received from user

    for event in pygame.event.get(): # Quits the program if the application is closed
        if event.type == QUIT:
            quitgame()
        
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
                pygame.event.post(pygame.event.Event(QUIT)) # Quits game if q or esc is pressed
    
    # Translates key pressed to int
    move = game.direction_to_int(direction) 
    return move


# Main function - Entry point into program
if __name__ == "__main__":
    kick_start(background) # loading screen
    team_logo_display() # loads logo
    
    pygame.mixer.music.load('./sound/background.mp3')
    pygame.mixer.music.play(-1)
    
    initial_interface() # Loads main menu
