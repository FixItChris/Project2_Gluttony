# -*- coding: utf-8 -*-

# Importing necessary modules
import pygame, random
import numpy as np

pygame.init() # Initialise pygame module

# Modification - Added sound effect for eating food
point_collect = pygame.mixer.Sound('./sound/point_collect.wav')

# Defines properties of the screen
class Settings:
    def __init__(self):
        self.width = 28 # Number of squares from left to right in the grid
        self.height = 28 # Number of squares from top to bottom on the grid
        self.rect_len = 15 # Width/height of square icons used during gameplay (in px)


# Defines snake mechanics and visual assets, including simulation of movement
class Snake:
    def __init__(self):
        # Loading of all images of the snake's head (up/down/left/right)
        self.image_up = pygame.image.load('images/head_up.bmp')
        self.image_down = pygame.image.load('images/head_down.bmp')
        self.image_left = pygame.image.load('images/head_left.bmp')
        self.image_right = pygame.image.load('images/head_right.bmp')

        # Loading of all images of the snake's tail (up/down/left/right)
        self.tail_up = pygame.image.load('images/tail_up.bmp')
        self.tail_down = pygame.image.load('images/tail_down.bmp')
        self.tail_left = pygame.image.load('images/tail_left.bmp')
        self.tail_right = pygame.image.load('images/tail_right.bmp')
        
        # Loading image of snake's body - to be used for all other sections of snake
        self.image_body = pygame.image.load('images/body.bmp')

        # Calls initialize function below
        self.initialize()
    
    # Sets snake's starting position, and initialises the user's score
    def initialize(self):
        self.position = [6, 6] # Position of head
        self.segments = [[6 - i, 6] for i in range(3)] # Position of entire snake on grid
        self.score = 0 # Sets/resets user score to 0
        self.facing = "right" # Sets snake to be facing to the right (Modification - Bug Fix)
    
    # Moves snake's body components on screen
    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y)) # Loads and displays image on screen
    
    # Moves snake's head component on screen
    def blit_head(self, x, y, screen):
        # Checks which way the snake is facing (determined by user input)
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y))  
    
    # Moves snake's tail component on screen
    def blit_tail(self, x, y, screen):
        # Determines which way tail needs to be facing
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)] 
        
        # Checks which way tail needs to be facing after updating
        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))  
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))  
        else:
            screen.blit(self.tail_right, (x, y))  
    
    # Combines above 3 functions so that all components of the snake are moved
    def blit(self, rect_len, screen):
        # Updates head
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        
        # Updates body
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        
        # Updates tail
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)                
            
   
    # Updates position of snake's head by modifying position variable
    def update(self):
        # Input from user
        if self.facing == 'right': 
            self.position[0] += 1
        if self.facing == 'left': 
            self.position[0] -= 1
        if self.facing == 'up': 
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        
        # Updates list containing each part of the snake
        self.segments.insert(0, list(self.position))


# Defines mechanics of the strawberry on the board
class Strawberry():
    def __init__(self, settings):
        self.settings = settings # Stores settings from class given as input
        
        # Randomly selects image of food to display on screen
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')
        self.initialize() # Sets initial position of strawberry
    
    # Defines random position to place new strawberry
    def random_pos(self, snake):
        # Randomly selects image of food to display on screen
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')                
        
        # Randomly selects position of food on board
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)
        
        if self.position in snake.segments: # If strawberry is placed where snake already is, try again
            self.random_pos(snake)

    # Displays image of strawberry on screen
    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    # Sets first position of food
    def initialize(self):
        self.position = [15, 10]


# Initialises all other previous classes, and defines functions for user input/overall gameplay
class Game:
    """
    """
    def __init__(self):
        self.settings = Settings() # Initialises Settings class above
        self.snake = Snake() # Initialises Snake class above
        self.strawberry = Strawberry(self.settings) # Initialises Strawberry class above
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'} # Defines possible keyboard inputs
        
    # Resets to initial values of the snake/strawberry when starting new game
    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()
    
    # Defines current state of the snake and strawberry during gameplay (CURRENTLY UNUSED)
    def current_state(self):         
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
    
    # Converts user arrow key input into a specific integer (defined in move_dict)
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()} # Reverses key:value pairs in dict
        return direction_dict[direction] # Returns integer representation
    
    # Implements main game logic - user input, if the snake consumes the food, if the game is finished
    def do_move(self, move):
        move_dict = self.move_dict
        
        change_direction = move_dict[move] # Defined by user input
        
        # Checks the user input and that the input is valid, then updates the direction of the snake's head
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction
        
        self.snake.update()
        
        # Checks if snake consumes the food
        if self.snake.position == self.strawberry.position:
            pygame.mixer.Sound.play(point_collect) # Sound effect defined above
            self.strawberry.random_pos(self.snake) # Finds new position to put next strawberry
            reward = 1
            self.snake.score += 1 # Updates user score
        else:
            self.snake.segments.pop() # Removes last segment (tail) from snake so that it stays the same length
            reward = 0
                
        if self.game_end(): # Checks lose conditions (below)
            return -1
                    
        return reward


    # Checks if the game is finished (snake has crashed)
    def game_end(self):
        end = False
        # Crashes against left/right border
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0: 
            end = True
        # Crashes against top/bottom border   
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0: 
            end = True
        # Crashes into itself
        if self.snake.segments[0] in self.snake.segments[1:]: 
            end = True

        return end

    # Updates score accordingly
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25) # Sets font
        text = font.render('Score: ' + str(self.snake.score), True, color) # Score text
        screen.blit(text, (0, 0)) # Shows score on screen, in top left corner
    
