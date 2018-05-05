import random
#all the constants
screen_size = [0,0]
colors = {'black':(0,0,0),'white':(255,255,255),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255),'background': (0,0,0)}
MOVE_STILL = 0 #this is for checking if thep layer is not moving.
MOVE_UP = 1 #this is for movement up
MOVE_DOWN = 2 #and this one is down
#setters for the constants
def set_screen_size(width,height):
    screen_size[0] = width
    screen_size[1] = height
def screen_percent(percent, **from_end):
    '''takes a percent of the screen and return the amount of pixels. if from_end = True, the it return the amount of pixels from end'''
    if from_end:
        backwards = 100-percent #calcualtes the percent from end (i.e. 90% becomes 10%)
        return float(screen_size[0]*backwards)/100 , float(screen_size[1]*backwards)/100
    else:
        return float(screen_size[0]*percent)/100 , float(screen_size[1]*percent)/100
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