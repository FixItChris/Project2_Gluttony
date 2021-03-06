# Importing necessary modules
import pygame, random
import numpy as np
import config
import sys, os

# Modification - Compiling into executable
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))

    return os.path.join(base_path, relative_path)

pygame.init() # Initialise pygame module

# Modification - Added sound effect for eating food
point_collect = pygame.mixer.Sound(resource_path('sound/eating_regular_fruit.mp3'))
mushroom_fast = pygame.mixer.Sound(resource_path('sound/fast_mushroom.mp3'))
mushroom_slow = pygame.mixer.Sound(resource_path('sound/slow_mushroom.mp3'))
super_sound = pygame.mixer.Sound(resource_path('sound/super_fruit.mp3'))
potion_sound = pygame.mixer.Sound(resource_path('sound/potion.mp3'))
crash_into_sound = pygame.mixer.Sound(resource_path('sound/crashes_into_itself.mp3'))

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
        self.image_up = pygame.image.load(resource_path('images/head_up.png'))
        self.image_down = pygame.image.load(resource_path('images/head_down.png'))
        self.image_left = pygame.image.load(resource_path('images/head_left.png'))
        self.image_right = pygame.image.load(resource_path('images/head_right.png'))

        # Loading of all images of the snake's tail (up/down/left/right)
        self.tail_up = pygame.image.load(resource_path('images/tail_up.png'))
        self.tail_down = pygame.image.load(resource_path('images/tail_down.png'))
        self.tail_left = pygame.image.load(resource_path('images/tail_left.png'))
        self.tail_right = pygame.image.load(resource_path('images/tail_right.png'))
        
        # Loading image of snake's body - to be used for all other sections of snake
        self.image_body = pygame.image.load(resource_path('images/body.png'))

        # Calls initialize function below
        self.initialize()
    
    # Sets snake's starting position, and initialises the user's score
    def initialize(self):
        self.position = [6, 6] 
        self.segments = [[6 - i, 6] for i in range(3)] 
        self.score = 0 
        self.facing = "right" # Modification - Spawn kill bug fix
    
    # Modification - Restart game using potion
    def new_life(self):
        self.position = [6, 6]
        self.segments = [[6 - i, 6] for i in range(self.score+3)]
        self.facing = "right"
    
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
        j = 0
        while True:
            # Determines which way tail needs to be facing
            tail_direction = [self.segments[-2-j][i] - self.segments[-1-j][i] for i in range(2)] 

            # Checks which way tail needs to be facing after updating
            if tail_direction == [0, -1]:
                screen.blit(self.tail_up, (x, y))
                break
            elif tail_direction == [0, 1]:
                screen.blit(self.tail_down, (x, y))
                break
            elif tail_direction == [-1, 0]:
                screen.blit(self.tail_left, (x, y))
                break
            elif tail_direction == [1, 0]:
                screen.blit(self.tail_right, (x, y))
                break
            j += 1
    
    # Combines above 3 functions so that all components of the snake are moved
    def blit(self, rect_len, screen):
        # Updates head
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len+25, screen)                
        
        # Updates body
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len+25, screen)
        
        # Updates tail
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len+25, screen)                
            
   
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
        self.image = pygame.image.load(resource_path('images/fruit.png'))
        self.initialize() # Sets initial position of strawberry
    
    # Defines random position to place new strawberry
    def random_pos(self, snake):
        # Randomly selects image of food to display on screen
        self.image = pygame.image.load(resource_path('images/fruit.png'))

        # Randomly selects position of food on board
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)
       
        # If strawberry is placed where snake already is, try again
        if self.position in snake.segments: 
            self.random_pos(snake)

    # Displays image of strawberry on screen
    def blit(self, screen):
        rect_len = self.settings.rect_len
        screen.blit(self.image, [self.position[0]*rect_len, self.position[1]*rect_len+25])
   
    # Sets first position of food
    def initialize(self):
        self.position = [15, 10]

# Modification - Mushroom special food
class Mushroom(Strawberry):
    def __init__(self, settings):
        super().__init__(settings)
        self.image = pygame.image.load(resource_path('images/mushroom.png'))
    
    def random_pos(self, snake):
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        if self.position in snake.segments:
            self.random_pos(snake)

# Modification - Super fruit
class Super_Fruit(Strawberry):
    def __init__(self, settings):
        super().__init__(settings)
        self.image = pygame.image.load(resource_path('images/super_fruit.png'))
    
    def random_pos(self, snake):
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        if self.position in snake.segments:
            self.random_pos(snake)

# Modification - Potion
class Potion(Strawberry):
    def __init__(self, settings):
        super().__init__(settings)
        self.image = pygame.image.load(resource_path('images/snake_potion.png'))
    
    def random_pos(self, snake):
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        if self.position in snake.segments:
            self.random_pos(snake)
 

# Initialises all other previous classes, defines functions for user input/overall gameplay
class Game:
    def __init__(self):
        self.settings = Settings() # Initialises Settings class above
        self.snake = Snake() # Initialises Snake class above
        self.strawberry = Strawberry(self.settings) # Initialises Strawberry class above
        self.mushroom = Mushroom(self.settings)
        self.super_fruit = Super_Fruit(self.settings)
        self.potion = Potion(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'} # Defines possible keyboard inputs
        
    # Resets to initial values of the snake/strawberry when starting new game
    def restart_game(self):
        if config.new_life:
            self.snake.new_life()
        else:
            self.snake.initialize()
        self.strawberry.initialize()
        config.mushroom_out = 0
        config.super_fruit_out = 0
        config.potion_out = 0
        config.has_potion = 0 
    

    # Converts user arrow key input into a specific integer (defined in move_dict)
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
    
    # Main game logic - checks user input, if the snake consumes food, if the game is finished
    def do_move(self, move, screen):
        move_dict = self.move_dict
        
        change_direction = move_dict[move] # Defined by user input
        
        # Checks for valid input, then updates the direction of the snake's head
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
       
            # Modification - Special fruit chances
            rng = random.randint(0,100)
            if rng > 95 and not config.potion_out and not config.has_potion:
                config.potion_out = 1
                self.potion.random_pos(self.snake)
                self.potion.blit(screen)

            elif rng <= 10 and not config.super_fruit_out:
                config.super_fruit_out = 1
                self.super_fruit.random_pos(self.snake)
                self.super_fruit.blit(screen)
            
            elif rng <= 25 and rng > 10 and not config.mushroom_out:
                config.mushroom_out = 1
                self.mushroom.random_pos(self.snake)
                self.mushroom.blit(screen)

        # Modification - Mechanics of special fruits
        elif self.snake.position == self.potion.position and config.potion_out:
            pygame.mixer.Sound.play(potion_sound)
            config.potion_out = 0
            config.has_potion = 1
            reward = 2

        elif self.snake.position == self.super_fruit.position and config.super_fruit_out:
            pygame.mixer.Sound.play(super_sound)
            config.super_fruit_out = 0
            reward = 3
            self.snake.score += 3
            for i in range(2):
                self.snake.segments.append(self.snake.segments[-1])

        elif self.snake.position == self.mushroom.position and config.mushroom_out:
            config.mushroom_out = 0
            reward = 4
            
            if random.randint(0,1) or config.fps<=5:
                config.fps += 3
                pygame.mixer.Sound.play(mushroom_fast)
            else:
                config.fps -= 3
                pygame.mixer.Sound.play(mushroom_slow)
        
        else:
            # Removes last segment (tail) from snake so that it stays the same length
            self.snake.segments.pop() 
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
            crash_into_sound.play()
            end = True

        return end

    # Updates score accordingly
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25) # Sets font
        text = font.render('Score: ' + str(self.snake.score), True, color) # Score text
        screen.blit(text, (5, 5)) # Shows score on screen, in top left corner


    
