import pygame
import random
#all the constants
screen_size = [0,0]
colors = {'black':(0,0,0),'white':(255,255,255),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255),'background': (0,0,0)}
MOVE_STILL = 0 #this is for checking if the player is not moving.
MOVE_UP = 1 #this is for movement up
MOVE_DOWN = 2 #and this one is down
keys = {'FIRST_PLAYER_UP':pygame.K_a,'FIRST_PLAYER_DOWN':pygame.K_d,'SECOND_PLAYER_UP':pygame.K_RIGHT,'SECOND_PLAYER_DOWN':pygame.K_LEFT}
#setters for the constants
def set_screen_size(width,height):
    screen_size[0] = width
    screen_size[1] = height
def surface_percent(percent,from_end=False,rect = None):
    '''takes a percent of the screen and return the amount of pixels. if from_end = True, the it return the amount of pixels from end
       is also able to take an extra parameter called rect. rect is a list/tuple that looks like this: [x,y,w,h]. it will return the amount of pixels from this rect'''
    if rect is None:
        rect = 0,0,screen_size[0],screen_size[1]
    if from_end:
        backwards = 100-percent #calcualtes the percent from end (i.e. 90% becomes 10%)
        return rect[0]+(float(rect[2]*backwards)/100) , rect[1]+(float(rect[3]*backwards)/100)
    else:
        return rect[0]+(float(rect[2]*percent)/100) , rect[1]+(float(rect[3]*percent)/100)
def walls():
    '''this return a list of dictionaries that represent the bounds of the game'''
    up = {'x': 0,'y': -50,'w': screen_size[0] ,'h':50,'color': colors['background'],'id':'up'}
    down = {'x': 0,'y': screen_size[1],'w': screen_size[0] ,'h':50,'color': colors['background'],'id':'down'}
    left = {'x': -50,'y': 0,'w': 50 ,'h':screen_size[1],'color': colors['background'],'id':'left'}
    right = {'x': screen_size[0] , 'y': 0, 'w': 50 , 'h': screen_size[1], 'color': colors['background'], 'id': 'right'}
    return [up,down,left,right]
def set_color(name_of_color,color):
    colors[name_of_color] = color
def random_color():
    return random.randrange(256),random.randrange(256),random.randrange(256)