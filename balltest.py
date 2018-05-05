import pygame
import math
from constants import * #this holds all the variables and their setters
pygame.init()
BACKGROUND_COLOR = (0,0,0)
def move(ball,blocks,players):
    #this moves the players
    for player in players:
        if player['movement'] == MOVE_DOWN:
            player['y']+=5
        if player['movement'] == MOVE_UP:
            player['y']-=5
    rang = math.radians(ball['ang'])
    move_x = int(round(ball['speed']*math.cos(rang)))
    move_y = int(round(ball['speed']*math.sin(rang)))
    #there are two different loops that seem identical, but they are here so that the movement feels more natural
    counter = abs(move_y)  # I need to keep the value of move_x but i also need to decrease it so here is a counter
    while counter != 0:
        id = 0  # this counts the place of the object in the array
        for block in blocks:
            collided,direction = collide(ball, block) #this is saved so I can use the direction later
            if collided:
                ball['x'] = int(round(ball['x']-math.copysign(float(move_x)/move_y,move_x)))
                ball['y'] = int(round(ball['y']-math.copysign(1,move_y)))
                return id, direction
            id += 1
        ball['x'] += math.copysign(float(move_x)/move_y,move_x)
        ball['y'] += math.copysign(1,move_y)
        counter -= 1
    ball['x'] = int(round(ball['x']))
    ball['y'] = int(round(ball['y']))
    return -1, "NaN"
def simple_move(ball,speed = 0,ang = 0):
    '''the difference between this movement method and the 'move' command is that this lacks collision detection'''
    if speed==0:
        speed = ball['speed']
    if ang==0:
        ang = ball['ang']
    rang = math.radians(ang)
    ball['x'] += round(speed*math.cos(rang))
    ball['y'] += round(speed*math.sin(rang))
def round(num):
    if num%1 >= 0.5:
        return int(math.ceil(num))
    return int(math.floor(num))
def near(num1,num2,difference):
    '''checks if the first number is near the second number by the number provided.
        for example: near(2,4,1) returns True because: (2<=4<=2+1 or 2-1<=4<=2) equals (False or True) equals True'''
    return num1<=num2<=num1+difference or num1-difference<=num2<=num1
def collide(ball,object):
    '''returns a tuple containing a boolean (did the ball hit something?) and a string that represents direction of hit (x or y) '''
    if 'r' in object:
        return math.sqrt((math.fabs(ball['x']-object['x'])**2) + (math.fabs(ball['y']-object['y'])**2)) <= ball['r']
    else:
        if near(ball['x']+ball['r'],object['x'],2) or near(ball['x']-ball['r'],object['x']+object['w'],2):
            return object['y'] <= ball['y'] <= object['y'] + object['h'] , 'x'
        if near(ball['y']+ball['r'],object['y'],2) or near(ball['y']-ball['r'],object['y']+object['h'],2):
            return object['x'] <= ball['x'] <= object['x'] + object['w'] , 'y'
        return False,"NaN"
def change_direction(ball,direction):
    '''takes a ball object and also the direction of the hit (x or y)'''
    if direction == 'x':
        ball['speed']*=-1
        ball['ang']*=-1
    else:
        ball['ang']*=-1
def add_block(blocks,x,y,w,h,color):
    blocks.append({'x':x,'y':y,'w':w,'h':h,'color':color,'id':len(blocks)})
def draw(screen, balls, blocks):
    screen.fill(BACKGROUND_COLOR)
    for ball in balls:
        pygame.draw.circle(screen,ball['color'],(ball['x'],ball['y']),ball['r'],0)
    for obj in blocks:
        pygame.draw.rect(screen,obj['color'],(obj['x'],obj['y'],obj['w'],obj['h']),0)
    pygame.display.flip()
def main():
    screen = pygame.display.set_mode((600, 600))
    set_screen_size(screen.get_width(), screen.get_height())
    TIMEREVENT = pygame.USEREVENT+1
    ball = {'x':100,'y':150,'r':10,'color':(56,250,143),'speed':10,'ang':20,'stuck':False}
    balls = [ball]
    player = {'x':screen_percent(5)[0],'y': 0,'w':25,'h':100,'color':random_color(),'id':"player",'movement':MOVE_STILL}
    blocks = [] #this holds the data of all the blocks (not including the walls). each blocks place in the list coressponds to its ID.
    #set_screen_size(screen.get_width(),screen.get_height())
    pygame.time.set_timer(TIMEREVENT,16)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player['movement'] = MOVE_UP
                elif event.key == pygame.K_s:
                    player['movement'] = MOVE_DOWN
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player['movement'] = MOVE_STILL
            if event.type == TIMEREVENT:
                for ball in balls:
                    id,direction = move(ball,blocks+walls()+[player],[player]) #this is saved so that the object can removed from the game later
                    if direction!="NaN":
                        print direction
                    if id != -1:
                        change_direction(ball,direction)
                    draw(screen, balls, blocks+[player])
    pygame.quit()
main()