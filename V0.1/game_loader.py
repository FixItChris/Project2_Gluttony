from faulthandler import disable
from string import whitespace
import pygame, time, random
import os
from multiprocessing import *
import subprocess
import sys

open_directory = os.getcwd()
print(open_directory)

def import_and_install(package):
    try:
        return __import__(package)
    except ImportError:
        return None
        
import_and_install('numpy')
import_and_install('pygame')

def program_start_another(program, exit_code=0):
    subprocess.Popen(program)
    sys.exit()

pygame.init()

pygame.display.set_caption('Pygame: Loading - Gluttonous')

black = [0, 0, 0]
green = [100, 255, 0]
white = [255, 255, 255]

font_descript = pygame.font.SysFont("arial", 10, True)

display_width = 420
display_height = 420

size = [display_width, display_height]
screen = pygame.display.set_mode(size)
background = pygame.image.load('./logos/gamelogo.png')

clock = pygame.time.Clock()

progress = 0 

def kick_start(progress, background):
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

if __name__ == "__main__":
    kick_start(progress, background)
    program_start_another(['python3', './main.py'])
