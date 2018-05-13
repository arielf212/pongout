import pygame
import random
#all the constants
screen_size = [0,0]
colors = {'black':(0,0,0),'white':(255,255,255),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255),'background': (0,0,0)}
MOVE_STILL = 0 #this is for checking if the player is not moving.
MOVE_UP = 1 #this is for movement up
MOVE_DOWN = 2 #and this one is down
keys = {'FIRST_PLAYER_UP':pygame.K_w,'FIRST_PLAYER_DOWN':pygame.K_s,'SECOND_PLAYER_UP':pygame.K_RIGHT,'SECOND_PLAYER_DOWN':pygame.K_LEFT}
#setters for the constants
def set_screen_size(width,height):
    screen_size[0] = width
    screen_size[1] = height
def surface_percent(percent,from_end=False,dimensions = None):
    '''takes a percent of the screen and return the amount of pixels. if from_end = True, the it return the amount of pixels from end
       is also able to take an extra parameter called rect. rect is a list/tuple that looks like this: [x,y,w,h]. it will return the amount of pixels from this rect'''
    if dimensions is None:
        dimensions = screen_size
    if from_end:
        backwards = 100-percent #calcualtes the percent from end (i.e. 90% becomes 10%)
        return float(dimensions[0]*backwards)/100 , float(dimensions[1]*backwards)/100
    else:
        return float(dimensions[0]*percent)/100 , float(dimensions[1]*percent)/100
def create_players():
    players = []
    for x in range(2):
        h = surface_percent(16.67,from_end=bool(x))[1] #the percent doesnt mean anything, I just like how it looks.
        w = h/4 #this makes the player proportions fell good
        x = surface_percent(5)[0]
        y = surface_percent(50)[1] - (h/2) #this is so that the player starts in the middle of the screen
        players.append({'x':x,'y':y,'w':w,'h':h,'color':random_color(),'rect':[x,y,w,h],'movement':MOVE_STILL})
    return players
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