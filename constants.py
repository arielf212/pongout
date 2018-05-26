import pygame
import random
import math
#all the constants
screen_size = [0,0]
colors = {'black':(0,0,0),'white':(255,255,255),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255),'background': (0,0,0)}
MOVE_STILL = 0 #this is for checking if the player is not moving.
MOVE_UP = 1 #this is for movement up
MOVE_DOWN = 2 #and this one is down
keys = {'LEFT_PLAYER_UP':pygame.K_w,'LEFT_PLAYER_DOWN':pygame.K_s,'RIGHT_PLAYER_UP':pygame.K_UP,'RIGHT_PLAYER_DOWN':pygame.K_DOWN}
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
#setters for the constants
def set_screen_size(width,height):
    screen_size[0] = width
    screen_size[1] = height
def surface_percent(percent,from_end=False,from_start_of_surface = False,rect = None):
    '''takes a percent of the screen and return the amount of pixels. if from_end = True, the it return the amount of pixels from end
       is also able to take an extra parameter called rect. rect is a list/tuple that looks like this: [x,y,w,h]. it will return the amount of pixels from this rect'''
    if rect is None:
        rect = [0,0,screen_size[0],screen_size[1]]
    if from_end:
        percent = 100-percent #calcualtes the percent from end (i.e. 90% becomes 10%)
    return rect[0]*from_start_of_surface+float(rect[2]*percent)/100 , rect[1]*from_start_of_surface+float(rect[3]*percent)/100
def round(num):
    if num%1 >= 0.5:
        return int(math.ceil(num))
    return int(math.floor(num))
def create_players():
    players = []
    side = ['LEFT','RIGHT'] #this will be used inside the main event loop to determine the buttons the palayer will be using (player['side'] + '_PLAYER_DOWN)
    for player in range(2):
        h = round(surface_percent(16.67)[1]) #the percent doesnt mean anything, I just like how it looks.
        w = h/4 #this makes the player proportions fell good
        x = round(surface_percent(5,from_end=bool(range(player)))[0])
        if player == 1:
            x-=w #this is here to make the players look symetrical.
        y = round(surface_percent(50)[1] - (h/2)) #this is so that the player starts in the middle of the screen
        players.append({'x':x,'y':y,'w':w,'h':h,'color':random_color(),'rect':[x,y,w,h],'movement':MOVE_STILL,'side':side[player]})
    print players
    return players
def create_left_ball(player_left,angle):
    x = player_left['x']+player_left['w']+20
    y = round(surface_percent(50,from_start_of_surface=True,rect=player_left['rect'])[1])
    return {'x':x, 'y':y, 'r':10, 'color' : random_color(), 'speed' : 10*1.5, 'ang': angle} #change later so that speed is 'r'*2
def create_right_ball(player_right,angle):
    x = player_right['x']-20
    y = round(surface_percent(50,from_start_of_surface=True,rect=player_right['rect'])[1])
    return {'x': x, 'y': y, 'r': 10, 'color': random_color(), 'speed' : 10*-2, 'ang': angle}
def create_angle_line(obj,ang,line_len=50):
    '''obj is the object the line is going from.
       ang is the angle of the line
       returns the line in a [(x,y),(x,y)] format'''
    rang = math.radians(ang)
    if 'r' in obj:
        print 'TODO: angle line from ball'
    else:
        start_pos = surface_percent(50,from_start_of_surface=True,rect = obj['rect']) # x,y tuple
        end_pos = line_len*math.cos(rang) , line_len*math.sin(rang) #len_x , len_y tuple
        return [(start_pos[0],start_pos[1]),(start_pos[0]+end_pos[0],start_pos[1]+end_pos[1])]
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
    return [random.randrange(256) for x in range(3)]
