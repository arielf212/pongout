import pygame
import math
from constants import * #this holds all the variables and their setters
pygame.init()
BACKGROUND_COLOR = (0,0,0)
def move(screen,ball,blocks,players):
    #this moves the players
    rang = math.radians(ball['ang'])
    move_x = round(ball['speed']*math.cos(rang))
    move_y = round(ball['speed']*math.sin(rang))
    #there are two different loops that seem identical, but they are here so that the movement feels more natural
    counter = abs(move_y)  # I need to keep the value of move_x but i also need to decrease it so here is a counter
    while counter != 0:
        id = 0  # this counts the place of the object in the array
        for block in blocks:
            collided,direction = collide(ball, block) #this is saved so I can use the direction later
            if collided:
                while collided:
                    ball['x'] = round(ball['x']-math.copysign(float(move_x)/move_y,move_x))
                    ball['y'] = round(ball['y']-math.copysign(1,move_y))
                    collided = collide(ball,block)[0]
                return id, direction
            id += 1
        ball['x'] += math.copysign(float(move_x)/move_y,move_x)
        ball['y'] += math.copysign(1,move_y)
        counter -= 1
    ball['x'] = round(ball['x'])
    ball['y'] = round(ball['y'])
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
        if ball['x']<=object['x']<=ball['x']+ball['r'] or ball['x']-ball['r']<=object['x']+object['w']<=ball['x']:
            return object['y'] <= ball['y'] <= object['y'] + object['h'] , 'x'
        if ball['y']<=object['y']<=ball['y']+ball['r'] or ball['y']-ball['r']<=object['y']+object['h']<=ball['y']:
            return object['x'] <= ball['x'] <= object['x'] + object['w'] , 'y'
        if object['x'] <= ball['x'] <= object['x'] + object['w'] and object['y'] <= ball['y'] <= object['y'] + object['h']:
            return True,"corner"
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
def dictate_angle(screen,player1,player2):
    #all of these are booleans for button holding
    first_up = False
    first_down = False
    second_up = False
    second_down = False

    #timer events
    COUNTDOWNEVENT = pygame.USEREVENT + 1
    MOVEEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(COUNTDOWNEVENT,1000)
    pygame.time.set_timer(MOVEEVENT,16)
    countdown = 10
    angle = 0
    while countdown>=0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                print first_up, first_down
                if event.key == keys['FIRST_PLAYER_UP']:
                    first_up = True
                if event.key == keys['FIRST_PLAYER_DOWN']:
                    first_down = True
                if event.key == keys['SECOND_PLAYER_UP']:
                    second_up = True
                if event.key == keys['SECOND_PLAYER_DOWN']:
                    second_down = True
            elif event.type == pygame.KEYUP:
                print first_up,first_down
                if event.key == keys['FIRST_PLAYER_UP']:
                    first_up = False
                if event.key == keys['FIRST_PLAYER_DOWN']:
                    first_down = False
                if event.key == keys['SECOND_PLAYER_UP']:
                    second_up = False
                if event.key == keys['SECOND_PLAYER_DOWN']:
                    second_down = False
            elif event.type == COUNTDOWNEVENT:
                print countdown
                countdown-=1
            elif event.type == MOVEEVENT:
                if first_up:
                    angle+=1
                if first_down:
                    angle-=1
                #calculate place of the line
                rang = math.radians(angle)
                start_pos = surface_percent(50,rect=[player1['x'],player1['y'],player1['w'],player1['h']])
                end_pos = start_pos[0]+50*math.cos(rang), start_pos[1]+50*math.sin(rang)
                screen.fill((0,0,0))
                pygame.draw.rect(screen, player1['color'], (player1['rect']), 0)
                pygame.draw.line(screen,(255,255,255),start_pos,end_pos,3)
                pygame.display.flip()
    return angle
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
    player = {'x':surface_percent(5)[0],'y': surface_percent(50)[1]-50,'w':25,'h':100,'color':random_color(),'id':"player",'movement':MOVE_STILL}
    player['rect'] = [player['x'],player['y'],player['w'],player['h']] #this is for the ball spawn
    blocks = [] #this holds the data of all the blocks (not including the walls). each blocks place in the list coressponds to its ID.
    ball = {'x': 50, 'y': 130, 'r': 10, 'color': (56, 250, 143), 'speed': 10, 'ang': dictate_angle(screen, player,player)}
    balls = [ball]
    pygame.time.set_timer(TIMEREVENT,16)
    running = True
    if ball['ang'] == 'quit':
        running = False
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
                    id,direction = move(screen,ball,blocks+walls()+[player],[player]) #this is saved so that the object can removed from the game later
                    for player in [player]:
                        if player['movement'] == MOVE_DOWN:
                            player['y']+=5
                        if player['movement'] == MOVE_UP:
                            player['y']-=5
                    if id != -1:
                        change_direction(ball,direction)
                    draw(screen, balls, blocks+[player])
    pygame.quit()
main()
