import pygame
import math
from constants import * #this holds all the variables and their setters
pygame.init()
BACKGROUND_COLOR = (0,0,0)
def move(screen,ball,blocks):
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
def dictate_angle(screen,player_left,player_right):
    #all of these are booleans for button holding
    left_up = False
    left_down = False
    right_up = False
    right_down = False

    #timer events
    COUNTDOWNEVENT = pygame.USEREVENT + 1
    MOVEEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(COUNTDOWNEVENT,1000)
    pygame.time.set_timer(MOVEEVENT,16)
    countdown = 10
    angle_left = 0
    angle_right = 0
    while countdown>=0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == keys['LEFT_PLAYER_UP']:
                    left_up = True
                if event.key == keys['LEFT_PLAYER_DOWN']:
                    left_down = True
                if event.key == keys['RIGHT_PLAYER_UP']:
                    right_up = True
                if event.key == keys['RIGHT_PLAYER_DOWN']:
                    right_down = True
                if event.key == pygame.K_SPACE:
                    countdown = 0
            elif event.type == pygame.KEYUP:
                if event.key == keys['LEFT_PLAYER_UP']:
                    left_up = False
                if event.key == keys['LEFT_PLAYER_DOWN']:
                    left_down = False
                if event.key == keys['RIGHT_PLAYER_UP']:
                    right_up = False
                if event.key == keys['RIGHT_PLAYER_DOWN']:
                    right_down = False
            elif event.type == COUNTDOWNEVENT:
                countdown-=1
            elif event.type == MOVEEVENT:
                if left_up and angle_left>=-60:
                    angle_left-=1
                elif left_down and angle_left<=60:
                    angle_left+=1
                elif right_up and angle_right>=-60:
                    angle_right-=1
                elif right_down and angle_right<=60:
                    angle_right+=1
                screen.fill((0,0,0))
                for x in range(2): # 2 players, 2 angles
                    player = [player_left,player_right][x]
                    angle = [angle_left,angle_right][x]
                    line_len = 50-(100*x) #left player needs the line to got left so the len is 50 and the right player needs the line to go right so the len is -50
                    angle_line = create_angle_line(player,angle,line_len = line_len) # [(x,y),(x,y)]
                    pygame.draw.rect(screen, player['color'], player['rect'], 0)
                    pygame.draw.line(screen,(255,255,255),angle_line[0],angle_line[1],3)
                pygame.display.flip()
    return {'left':angle_left,'right':angle_right}
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
    player_left,player_right = create_players()
    players = {}
    blocks = [] #this holds the data of all the blocks (not including the walls). each blocks place in the list coressponds to its ID.
    angles = dictate_angle(screen,player_left,player_right) # dict {'left','right'}
    ball_left = create_left_ball(player_left,angles['left'])
    ball_right = create_right_ball(player_right,angles['right'])
    balls = [ball_left,ball_right]
    pygame.time.set_timer(TIMEREVENT,16)
    running = True
    if ball_left['ang'] == 'quit' or ball_right['ang'] == 'quit':
        running = False
    while running:
        for event in pygame.event.get():
            for player in [player_left,player_right]:
                if event.type == pygame.KEYDOWN:
                    if event.key == keys[player['side']+'_PLAYER_UP']:
                        player['movement'] = MOVE_UP
                    elif event.key == keys[player['side']+'_PLAYER_DOWN']:
                        player['movement'] = MOVE_DOWN
                if event.type == pygame.KEYUP:
                    if event.key == keys[player['side']+'_PLAYER_UP'] or event.key == keys[player['side']+'_PLAYER_DOWN']:
                        player['movement'] = MOVE_STILL
            if event.type == TIMEREVENT:
                for ball in balls:
                    id,direction = move(screen,ball,blocks+walls()+[player_left,player_right]) #this is saved so that the object can removed from the game later
                    for player in [player_left,player_right]:
                        if player['movement'] == MOVE_DOWN:
                            player['y']+=5
                        if player['movement'] == MOVE_UP:
                            player['y']-=5
                    if id != -1:
                        change_direction(ball,direction)
                    draw(screen, balls, blocks+[player_left,player_right])
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
main()
