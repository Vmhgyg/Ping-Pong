from pygame import *
from random import randint

#Window and initiation
init()

length = 1050
height = 750

Window = display.set_mode((length,height))
display.set_caption("Pong")

clock = time.Clock()
FPS = 60

    #colours
BLACK = (0,0,0)
WHITE = (255,255,255)
PADDLEBALL = (240,240,240)
    
    #paddle, ball, and game variables
PAD_W, PAD_H = 15, 115
BALL_R = 12
PAD_SPEED = 13
BALL_SPEED_X = 11
BALL_SPEED_Y = 10
GAP_FROM_WALL = 30

pad1 = None
pad2 = None
ball = None


REQUIRE = 5
winner = None

score1 = 0
score2 = 0

paused = False

#-----------------------------------------------------------------------------

#UI

font.init()
score_font = font.Font(None,56)
hint_font = font.Font(None,28)

#-----------------------------------------------------------------------------

#Classes

class GameSprite(sprite.Sprite):
    def __init__(self, surf, x, y, speed=0):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def reset(self):
        Window.blit(self.image, self.rect.topleft)


class Player(GameSprite):
    def clamp(self):        #not off-screen
        if self.rect.top < 8:
            self.rect.top = 8
        if self.rect.bottom > height-8:
            self.rect.bottom = height-8

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        self.clamp()

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed
        self.clamp()


class Ball(GameSprite):
    def __init__(self, radius):
        surf = Surface((radius*2,radius*2), SRCALPHA)               #create a ball
        draw.circle(surf, PADDLEBALL, (radius,radius), radius)       #draws the ball
        super().__init__(surf, length//2 - radius, height//2 - radius, 0)
        self.vx = BALL_SPEED_X
        self.vy = BALL_SPEED_Y
        self.radius = radius
    
    def center_serve(self, direction=1):
        self.rect.center = (length//2 , height//2)
        self.vx = BALL_SPEED_X * direction
        self.vy = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
                                    #prevent sticking to wall
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)
            if self.vy == 0:
                self.vy = BALL_SPEED_Y
        
        elif self.rect.bottom >= height:
            self.rect.bottom = height
            self.vy = -abs(self.vy)
            if self.vy == 0:
                self.vy = -BALL_SPEED_Y




#-----------------------------------------------------------------------------

#Objects

paddle_surf = Surface((PAD_W, PAD_H))
paddle_surf.fill(PADDLEBALL)

racket1 = Player(paddle_surf.copy(), GAP_FROM_WALL, (height - PAD_H)//2, PAD_SPEED)
racket2 = Player(paddle_surf.copy(), length - GAP_FROM_WALL - PAD_W, (height - PAD_H)//2, PAD_SPEED)
ball = Ball(BALL_R)


#-----------------------------------------------------------------------------
#Functions

def draw_court():
    #background
    Window.fill(BLACK)

    #border
    draw.rect(Window, WHITE, Rect(8,8, length-16, height-16), width=4)

    #centre dashed line
    dash_h = 18
    gap_dash = 14
    x = length//2
    y = 8
    while y < height:
        draw.line(Window, WHITE, (x,y), (x,min(y+dash_h, height-8)), width=4)
        y += dash_h + gap_dash


def draw_ui():
    score_text = score_font.render(f"{score1}    :    {score2}", True, WHITE)
    Window.blit(score_text, (length//2 - score_text.get_width()//2, 16))

    if winner is not None:
        win_text = hint_font.render(f"Player {winner} wins, R to reset", True, WHITE)
        Window.blit(win_text, (length//2 - win_text.get_width()//2, 60))


def handle_paddle_collisions1():
    global ball

    if sprite.collide_rect(racket1,ball) and ball.vx <0:
            #separate to avoid sticking
        ball.rect.left = racket1.rect.right
            #reflect X
        ball.vx = abs(ball.vx)
            #add spin
        offset = (ball.rect.centery - racket1.rect.centery) / (racket1.rect.height / 2)
        ball.vy = max(-7, min(7, ball.vy + 4*offset))
    
    if sprite.collide_rect(racket2,ball) and ball.vx >0:
        ball.rect.right = racket2.rect.left
        ball.vx = -abs(ball.vx)
        offset = (ball.rect.centery - racket2.rect.centery) / (racket2.rect.height / 2)
        ball.vy = max(-7, min(7, ball.vy + 4*offset))



def handle_scoring():
    global score1, score2, winner, paused
    if ball.rect.left <= 0:
        score2 += 1
        ball.center_serve(direction=-1)
    elif ball.rect.right >= length:
        score1 += 1
        ball.center_serve(direction=-1)

    
    #win con
    if score1 >= REQUIRE or score2 >= REQUIRE:
        if score1 >= REQUIRE:
            winner = 1
        elif score2 >= REQUIRE:
            winner = 2
        paused = True





#-----------------------------------------------------------------------------

#Game Loop

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
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

    if paused:
        draw_court()
        draw_ui()
        pause_text = hint_font.render("P to pause | R to restart", True, WHITE)
        Window.blit(pause_text, (length//2 - pause_text.get_width()//2, height//2 -14))
        display.update()
        clock.tick(FPS)
        continue

#it displays it only after
#restting also does not work

    racket1.update_l()
    racket2.update_r()
    ball.update()

    handle_paddle_collisions1()
    handle_scoring()

#it cant pause tho

    draw_court()
    draw_ui()
    racket1.reset()
    racket2.reset()
    ball.reset()
    


    display.update()
    clock.tick(FPS)

quit()











