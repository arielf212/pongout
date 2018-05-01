import random
#all the constants
screen_size = [0,0]
colors = {'black':(0,0,0),'white':(255,255,255),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255)}
#setters for the constants
def set_screen_size(width,height):
    screen_size[0] = width
    screen_size[1] = height
def screen_percent(percent, **from_end):
    '''takes a percent of the screen and return the amount of pixels. if from_end = True, the it return the amount of pixels from end'''
    if from_end:
        print "TODO: add this."
    else:
        return (screen_size[0]*percent)/100,(screen_size[1]*percent)/100
def add_color(name_of_color,color,**is_opaque)
    colors[name_of_color]=color
def random_color():
    return random.randrange(256),random.randrange(256),random.randrange(256)
def