import pygame
import math
from constants import * #this holds all the variables and their setters
pygame.init()
BACKGROUND_COLOR = (0,0,0)
def move(ball, ang, speed, blocks):
    rang = math.radians(ang)
    move_x = round(speed*math.cos(rang))
    move_y = round(speed*math.sin(rang))
    if(move_x>move_y):
        counter = move_x  # I need to keep the value of move_x but i also need to decrease it so here is a counter
        while counter!=0:
            for block in blocks:
                if collide(ball,block):
                    print 'stop!'
                    ball['x'] = int(round(ball['x']))
                    ball['y'] = int(round(ball['y']))
                    return block['id']
            ball['x']+=1
            ball['y']+=move_y/move_x
            counter-=1
    else:
        counter = move_y  # I need to eep the value of move_x but i also need to decrease it so here is a counter
        while counter != 0:
            for block in blocks:
                if collide(ball, block):
                    ball['x'] = int(round(ball['x']))
                    ball['y'] = int(round(ball['y']))
                    return block['id']
            ball['x'] += move_x/move_y
            ball['y'] += 1
            counter -= 1
    ball['x'] = int(round(ball['x']))
    ball['y'] = int(round(ball['y']))
    return -1
    '''if ball['x'] > 600:
        ball['x'] = 600 - ball['r']
    elif ball['x'] < 0:
        ball['x'] = 0 + ball['r']
    if ball['y'] > 600:
        ball['y'] = 600 - ball['r']
    elif ball['y'] < 0:
        ball['y'] = 0 + ball['r']'''
def round(num):
    if num%1 >= 0.5:
        return math.ceil(num)
    return math.floor(num)
def collide(ball,object):
    '''ball_movement is a list containing the start and end point of the movement of the ball: [(start_x,start_ y),(end_x,end_y)]'''
    if 'r' in object:
        return math.sqrt((math.fabs(ball['x']-object['x'])**2) + (math.fabs(ball['y']-object['y'])**2)) <= ball['r']
    else:
        #print ball['x']+ball['r']==object['x'] , ball['x']-ball['r']==object['x']+object['w'] , ball['y']+ball['r']==object['y'] , ball['y']-ball['r']==object['y']+object['h']
        #print 'up',ball['y']+ball['r']<=object['y'] and object['x'] <= ball['x'] <= object['x'] + object['w'], 'left:', ball['x']+ball['r']<=object['x']and object['y'] <= ball['y'] <= object['y'] + object['h']
        if (ball['x']+ball['r']<=object['x'] or ball['x']-ball['r']<=object['x']+object['w']):
            return object['y'] <= ball['y'] <= object['y'] + object['h']
        if (ball['y']+ball['r']<=object['y'] or ball['y']-ball['r']<=object['y']+object['h']):
            return object['x'] <= ball['x'] <= object['x'] + object['w']
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
    TIMEREVENT = pygame.USEREVENT+1
    ball1 = {'x':100,'y':100,'r':10,'color':(200,45,132),'speed':10,'ang':20}
    ball2 = {'x':100,'y':150,'r':10,'color':(56,250,143),'speed':10,'ang':15}
    balls = [ball2]
    blocks = [] #this holds the data of all the blocks (not including the walls). each blocks place in the list coressponds to its ID.
    screen = pygame.display.set_mode((600,600))
    pygame.time.set_timer(TIMEREVENT,100)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                add_block(blocks,pos[0],pos[1],50,100,(132,43,11))
            elif event.type == TIMEREVENT:
                for ball in balls:
                    object_hit_id = move(ball,ball['ang'],ball['speed'],blocks) #this is saved so that the object is removed from the game later
                    if object_hit_id != -1:
                        balls.remove(ball)
                    if len(balls) == 0:
                        print 'stop!'
                        print ball1 , ball2, object_hit_id
                        return 1
                    draw(screen, balls, blocks)
    pygame.quit()
main()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()