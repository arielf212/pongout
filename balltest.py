from constants import * #this holds all the variables and their setters
import pygame , math
import random # this is for the random angle of the ball in the start scren
global screen # I need to use the screen both inside and outside functions
pygame.init()
#screen
screen = pygame.display.set_mode((0,0) , pygame.FULLSCREEN) # creating a screen
set_screen_size(screen.get_width(), screen.get_height()) #setting the screen size
BACKGROUND_COLOR = (0,0,0)
NUMBER_IMAGES = load_numbers()
def move(balls , blocks):
    destroy = [] # stores the placement of the blocks that the balls collided withz
    for ball in balls:
        ball['x'] += ball['move_x']
        ball['y'] += ball['move_y']
        for x in range(len(blocks)):
            collided , direction = collide(ball , blocks[x])
            if collided:
                ball['x'] -= ball['move_x']
                ball['y'] -= ball['move_y']
                change_direction(ball , direction)
                destroy.append(x)
                break
    return destroy
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
    rang = math.radians(ball['ang'])
    # recreate move_x and move_y with new values
    ball['move_x'] = ball['speed'] * math.cos(rang)
    ball['move_y'] = ball['speed'] * math.sin(rang)

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
    countdown = 5
    angle_left = 0
    angle_right = 0
    print score
    while countdown>=0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == keys['LEFT_PLAYER_UP']:
                    left_up = True
                if event.key == keys['LEFT_PLAYER_DOWN']:
                    left_down = True
                if event.key == keys['RIGHT_PLAYER_UP']:
                    right_up = True
                if event.key == keys['RIGHT_PLAYER_DOWN']:
                    right_down = True
                if event.key == keys['QUIT']:
                    return {'left':"quit",'right':'quit'} # the return has to be in this format or else it crashes
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
                if left_down and angle_left<=60:
                    angle_left+=1
                if right_up and angle_right<=60:
                    angle_right+=1
                if right_down and angle_right>=-60:
                    angle_right-=1
                screen.fill((0,0,0))
                for x in range(2): # 2 players, 2 angles
                    player = [player_left,player_right][x]
                    angle = [angle_left,angle_right][x]
                    direction = ['RIGHT','LEFT'][x]
                    angle_line = create_angle_line(player,angle,line_direction=direction) # [(x,y),(x,y)]
                    rect = [player['x'] , player['y'] , player['w'] , player['h']]
                    pygame.draw.rect(screen, player['color'], rect, 0)
                    pygame.draw.line(screen,(255,255,255),angle_line[0],angle_line[1],5)
                    screen.blit(NUMBER_IMAGES[countdown],(surface_percent(48)[0],0)) # loads the image that corresponds to the time
                pygame.display.flip()
    return {'left':angle_left,'right':angle_right}
def start_screen():
    global screen
    ball = {'x' : 10 , 'y' : surface_percent(50)[1] , 'r' : 10 , 'speed' : 15 , 'ang' : random.randint(-60,60) , 'color' : random_color()}
    TIMEREVENT = pygame.USEREVENT + 1  # this moves and redraws the screen every 16 ms
    pygame.time.set_timer(TIMEREVENT , 16)
    while -5 < ball['ang'] < 5:
        ball['ang'] = random.randint(-60 , 60) # if the angle is close to 0 the ball will just move horizontally forever
    rang = math.radians(ball['ang'])
    ball['move_x'] = ball['speed'] * math.cos(rang) #movement for the ball
    ball['move_y'] = ball['speed'] * math.sin(rang)
    wall = walls()
    start = pygame.image.load('start.png')
    title = pygame.image.load('title.png')
    sr = start.get_rect() # holder for the rect object
    tr = title.get_rect()
    sr.x = surface_percent(42)[0] # I have to update the cords or else they stay as 0,0
    sr.y = surface_percent(50)[1]
    tr.x = surface_percent(28)[0]
    tr.y = surface_percent(10)[1]
    start_rect = {'x' : surface_percent(42)[0] , 'y' : surface_percent(50)[1] , 'w' : sr.width , 'h' : sr.height} #this is for the collision with the ball
    title_rect = start_rect = {'x' : tr.x , 'y' : tr.y , 'w' : tr.width , 'h' : tr.height}
    while True:
        for event in pygame.event.get():
            if event.type == TIMEREVENT:
                move([ball] , [start_rect] + wall)
                screen.fill((0,0,0))
                screen.blit(start , (surface_percent(42)[0] , surface_percent(50)[1]))
                screen.blit(title , (surface_percent(28)[0] , surface_percent(10)[1]))
                pygame.draw.circle(screen,ball['color'],(round(ball['x']),round(ball['y'])),ball['r'],0)
                pygame.display.flip()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sr.collidepoint(pygame.mouse.get_pos()):
                    return 'play'
def draw(screen, balls, blocks):
    screen.fill(BACKGROUND_COLOR)
    for ball in balls:
        if ball['x'] == CHOOSE_ANGLE:
            direction = 'RIGHT' if ball['side'] =='LEFT' else 'LEFT'
            angle_line = create_angle_line(ball['player'] , ball['ang'] , line_direction=direction)
            pygame.draw.line(screen , (255,255,255) , angle_line[0] , angle_line[1] , 5)
        else:
            pygame.draw.circle(screen,ball['color'],(round(ball['x']),round(ball['y'])),ball['r'],0)
    for obj in blocks:
        pygame.draw.rect(screen,obj['color'],(round(obj['x']),round(obj['y']),obj['w'],obj['h']),0)
    pygame.display.flip()
def main(score_left = 0 , score_right = 0):
    global screen
    #variables
    blocks = [] # this holds the data of all the blocks (not including the walls or players). each blocks place in the list corresponds to its ID
    running = True
    #players and balls
    player_left,player_right = create_players()
    players = [player_left, player_right]
    angles = dictate_angle(screen,player_left,player_right) # dict {'left','right'}
    if angles['left'] == 'quit' or angles['right'] == 'quit':
        running = False
    else:
        ball_left = create_left_ball(player_left,angles['left'])
        ball_right = create_right_ball(player_right,angles['right'])
        player_left['ball'] = ball_left # sometimes I have to use the balls in a player-only function and vise versa
        player_right['ball'] = ball_right # so I am just giving the players and balls pointers to ach other
        balls = [ball_left,ball_right]
    #timers
    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT,16)
    while running:
        for event in pygame.event.get():
            for player in players:
                if event.type == pygame.KEYDOWN:
                    if event.key == keys[player['side']+'_PLAYER_UP']:
                        player['movement'] = MOVE_UP
                    if event.key == keys[player['side']+'_PLAYER_DOWN']:
                        player['movement'] = MOVE_DOWN
                    if event.key == keys[player['side']+'_BLOCK_SPAWN']:
                        ball = player['ball']
                        if ball['x'] == CHOOSE_ANGLE:
                            if ball['side'] == 'LEFT':
                                ball_left = create_left_ball(player, ball['ang'])  # we create a new ball since the old one got destroyed
                                player['ball'] = ball_left  # we add the new ball to the player
                                balls.append(ball_left)  # we add the new ball back to the "balls" list
                            else:
                                ball_right = create_right_ball(player , ball['ang'])
                                player['ball'] = ball_right
                                balls.append(ball_right)
                        else:
                            create_blocks(blocks,balls,ball)
                    if event.key == keys['QUIT']:
                        running = False
                if event.type == pygame.KEYUP:
                    if event.key == keys[player['side']+'_PLAYER_UP'] or event.key == keys[player['side']+'_PLAYER_DOWN']:
                        player['movement'] = MOVE_STILL
            if event.type == TIMEREVENT:
                for player in players:
                    if player['ball']['x'] == CHOOSE_ANGLE:
                        if player['side'] == 'LEFT':
                            player['ball']['ang'] = min(60 , max(-60 ,player['ball']['ang']+player['movement'])) # angle cant be more then 60 or less then -60
                        else:
                            player['ball']['ang'] = min(60, max(-60, player['ball']['ang']-player['movement']))
                    else:
                        player['y'] += 10 * player['movement'] # since the movements states are either -1 , 0 or 1 so MOVE_UP will make him move 5 up for example
                        for ball in balls:
                            if collide(ball , player)[0] or player['y'] < 5 or near(player['y']+player['h'] , screen_size[1] , 2):
                                player['y'] -= 10 * player['movement']
                                break
                destroy = move(balls , blocks+walls()+players) # this is the id of the blocks that I need to destroy
                for id in destroy:
                    if id < len(blocks): # to not get array out of bounds error since I am also checking collision with players and walls
                        del blocks[id] # removes the blocks that got hit
                    elif id-len(blocks) == LEFT: # walls come after blocks so we can check what is the wall by subtracting the id from the amount of blocks there is
                        if abs(ball_left['x']-walls()[LEFT]['x']) <= abs(ball_right['x']-walls()[LEFT]['x']): # we check which ball is the closest to the wall
                            print 'wtf'
                            ball_left['x'] = CHOOSE_ANGLE  # the ball enters the same state as in the "dictate_angle" function.
                            ball_left['ang'] = 0  # resets angle
                            balls.remove(ball_left)  # removes the ball from the "balls" list
                        else:
                            return (score_left,score_right+1) # we start the game again with a different score
                    elif id-len(blocks) == RIGHT:
                        if abs(ball_right['x'] - walls()[RIGHT]['x']) <= abs(ball_left['x'] - walls()[RIGHT]['x']):
                            ball_right['x'] = CHOOSE_ANGLE
                            ball_right['ang'] = 0
                            balls.remove(ball_right)
                        else:
                            return (score_left+1,score_right)

                draw(screen , [ball_left,ball_right] , players + blocks) # this function doesnt use the "balls" list since I want it
                pygame.display.flip()                                    # to use balls that don't exist anymore and those are deleted from the list
    return 'quit'
is quit = False
while not is_quit:
    score = (0,0) #left_score ,right_score
    if start_screen() == 'quit':
        is_quit = True
    while (score[0] < 9 or score[1] < 9) and not is_quit:
        timer = 0
        score = main(score_left=score[0],score_right=score[1])
        if score == 'quit':
            is_quit = True
            break
        screen.fill((0,0,0))
        screen.blit(NUMBER_IMAGES[score[0]] , surface_percent(35)) # 35% is in the close enough to the middle but not too much
        screen.blit(NUMBER_IMAGES[score[1]] , (surface_percent(35,from_end=True)[0],surface_percent(35 )[1]))
        pygame.display.flip()
        TIMEWAITEVENT = pygame.USEREVENT + 3 # this is to stop the game so that the user can see the score
        pygame.time.set_timer(TIMEWAITEVENT , 1000)
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == TIMEWAITEVENT:
                    wait = False
                    pygame.time.set_timer(TIMEWAITEVENT, 0) #disabling event for better performance
pygame.quit()
