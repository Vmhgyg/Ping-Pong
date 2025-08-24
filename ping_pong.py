from pygame import *


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
BALL_R = 10
PAD_SPEED = 13
BALL_SPEED_X = 10
BALL_SPEED_Y = 11
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

#-----------------------------------------------------------------------------

#Objects

paddle_surf = Surface((PAD_W, PAD_H))
paddle_surf.fill(PADDLEBALL)

racket1 = Player(paddle_surf.copy(), GAP_FROM_WALL, (height - PAD_H)//2, PAD_SPEED)
racket2 = Player(paddle_surf.copy(), length - GAP_FROM_WALL - PAD_W, (height - PAD_H)//2, PAD_SPEED)

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

    racket1.update_l()
    racket2.update_r()


    draw_court()
    draw_ui()
    racket1.reset()
    racket2.reset()
    display.update()
    clock.tick(FPS)












