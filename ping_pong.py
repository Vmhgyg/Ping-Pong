from pygame import *


#Window and initiation
init()

length = 700
height = 500

Window = display.set_mode((length,height))
display.set_caption("Pong")

clock = time.Clock()
FPS = 60

    #colours
BLACK = (0,0,0)
WHITE = (255,255,255)
PADDLEBALL = (240,240,240)
    
    #paddle, ball, and game variables
PAD_W, PAD_H = 15, 150
BALL_R = 10
PAD_SPEED = 20
BALL_SPEED_X = 10
BALL_SPEED_Y = 11
GAP_FROM_WALL = 30

REQUIRE = 5
winner = None

score1 = 0
score2 = 0

paused = False
#-----------------------------------------------------------------------------

#Functions

def draw_court():
    #background
    window.fill(BLACK)

    #border
    draw.rect(Window, LINES, Rect(8,8, length-16, height-16), width=4)

    #centre dashed line
    dash_h = 18
    gap_dash = 14
    x = length//2
    y = 8
    while y < height:
        draw.line(Window, LINES, (x,y), (x,min(y+dash_h, height-8),width = 4))
        y += dash_h + gap_dash










#-----------------------------------------------------------------------------

#Game Loop

game = True
while game:
    for e in event.get():
        if e.type == QUIT():
            game = False
        if e.type == KEY_DOWN:
            if e.type == K_ESCAPE:
                game == False
            if e.type == K_p:
                paused = not paused
            if e.type == K_r:
                score1 = score2 = 0
                winner = None
                pad1.rect.centery = height//2
                pad2.rect.centery = height//2
                ball.center_serve(direction=1)













