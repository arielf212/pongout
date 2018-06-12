import pygame
import random
import math
#all the constants
screen_size = [0,0]
colors = {'black':(0,0,0),'white':(255,255,255),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255),'background': (0,0,0)}
MOVE_STILL = 0 #this is for checking if the player is not moving
MOVE_UP = -1 #this is for movement up
MOVE_DOWN = 1 #and this one is down
keys = {'LEFT_PLAYER_UP':pygame.K_w,'LEFT_PLAYER_DOWN':pygame.K_s,'LEFT_BLOCK_SPAWN':pygame.K_SPACE,
        'RIGHT_PLAYER_UP':pygame.K_UP,'RIGHT_PLAYER_DOWN':pygame.K_DOWN,'RIGHT_BLOCK_SPAWN':pygame.K_RETURN,
        'QUIT' : pygame.K_ESCAPE}
UP = 0 #these are ofr taking specificx wlls form the "walls" function. for example: print walls()[UP]
DOWN = 1
LEFT = 2
RIGHT = 3
LEFT_BALL = 0 #this is for getting the balls from the 'balls' list
RIGHT_BALL = 1 # ^ same explanation
CHOOSE_ANGLE = -500 # this is the state a ball enter when it is removed from the game
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
def create_players(get_as_dict = False):
    '''creates the players. either return them as an array, or as a dict that looks like {'left','right'} if get_as_dect equals to True'''
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
    if get_as_dict:
        return {'left':players[0],'right':players[1]}
    return players
def create_left_ball(player_left,angle):
    rect = [player_left['x'] , player_left['y'] , player_left['w'] , player_left['h']]
    x = player_left['x']+player_left['w']+20 # I have to push it back or else it gets stuck inside the player
    y = round(surface_percent(50,from_start_of_surface=True,rect=rect)[1])
    rang =math.radians(angle)
    move_x = 10*math.cos(rang)
    move_y = 10*math.sin(rang)
    return {'x':x, 'move_x' : move_x , 'y':y, 'move_y' : move_y , 'r':10, 'speed' : 15, 'ang': angle , 'side' : 'LEFT' , 'player': player_left , 'color' : player_left['color']}
def create_right_ball(player_right,angle):
    rect = [player_right['x'], player_right['y'], player_right['w'], player_right['h']]
    x = player_right['x']-20
    y = round(surface_percent(50,from_start_of_surface=True,rect=rect)[1])
    rang = math.radians(angle)
    move_x = -10*math.cos(rang)
    move_y = -10*math.sin(rang)
    return {'x': x, 'move_x' : move_x , 'y': y, 'move_y' : move_y , 'r': 10,  'speed' : -15, 'ang': angle ,'side' : 'RIGHT', 'player' : player_right , 'color': player_right['color']}
def create_blocks(blocks,balls,ball):
    player = ball['player']
    blocks.append({'x': ball['x'], 'y': ball['y'], 'w': player['w'], 'h': player['h'], 'color': random_color()})  # creates block
    ball['x'] = CHOOSE_ANGLE  # the ball enters the same state as in the "dictate_angle" function.
    ball['ang'] = 0  # resets angle
    balls.remove(ball)  # removes the ball from the "balls" list
def create_angle_line(obj,ang,line_len=70 , line_direction = 'RIGHT'):
    '''obj is the object the line is going from.
       ang is the angle of the line
       returns the line in a [(x,y),(x,y)] format'''
    if line_direction == 'LEFT':
        line_len*=-1 #makes the line go the opposite way
    rang = math.radians(ang)
    rect = [obj['x'], obj['y'], obj['w'], obj['h']]
    start_pos = surface_percent(50,from_start_of_surface=True,rect = rect) # x,y tuple
    end_pos = line_len*math.cos(rang) , line_len*math.sin(rang) #len_x , len_y tuple
    return [(start_pos[0],start_pos[1]),(start_pos[0]+end_pos[0],start_pos[1]+end_pos[1])]
def walls():
    '''this return a list of dictionaries that represent the bounds of the game'''
    up = {'x': 0,'y': -50,'w': screen_size[0] ,'h':50,'color': colors['background']}
    down = {'x': 0,'y': screen_size[1],'w': screen_size[0] ,'h':50,'color': colors['background']}
    left = {'x': -50,'y': 0,'w': 50 ,'h':screen_size[1],'color': colors['background']}
    right = {'x': screen_size[0] , 'y': 0, 'w': 50 , 'h': screen_size[1], 'color': colors['background']}
    return [up,down,left,right]
def load_numbers():
    '''simply loads the number images'''
    number_images = []
    for number in ['zero','one','two','three','four','five','six','seven','eight','nine']:
        number_images.append(pygame.image.load('numbers/'+number+'.jpg'))
    return number_images
def set_color(name_of_color,color):
    colors[name_of_color] = color
def random_color():
    return [random.randrange(256) for x in range(3)]
