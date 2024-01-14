import pygame,sys
import random
from pygame.locals import*
from pygame import mixer
pygame.init()
mixer.init()

clock = pygame.time.Clock()

# Set up some image
bg = pygame.image.load("bg.png")
ground = pygame.image.load("ground.png")
bird2 = pygame.image.load("bird2.png")
pipe_img = pygame.image.load("pipe.png")
restart_img = pygame.image.load("restart.png")


# Set up screen 
width = 700
height = 600
screen = pygame.display.set_mode((width,height))
bg = pygame.transform.scale(bg,(width + 100,height-100))

pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(bird2)

#font 
font = pygame.font.SysFont(None,50)
font_point = pygame.font.SysFont('Bauhaus 93',70)

# set time for pipe
fps = 60
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - 1500
pipe_gap = 150
point = 0
pass_pipe = False
white = (255,255,255)

#background
bg_scroll = 0
bg_scroll_speed = 1
titles = 1

#ground
ground_scroll = 0
scroll_speed = 4

#play text
play_txt = "Click anywhere to play"
play_txt_img = font.render(play_txt,True,white)

#again


# over
game_over = False
once = True
flying = False
restart = False
clicked = False
x = restart_img.get_width()
again_rect = pygame.Rect((230, 240, restart_img.get_width(), restart_img.get_height()))

def stop_scr():
    global scroll_speed,bg_scroll_speed
    bg_scroll_speed = 0
    scroll_speed = 0

#set up bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range (1,4):
            img = pygame.image.load(f'bird{i}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.click = False
    def update(self):
        global game_over
        if game_over == False:
            self.counter += 5
            if self.counter >= 30:
                self.counter = 0
                self.index = (self.index + 1) % 3
                self.image = self.images[self.index]
            if flying == True:
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8
                if self.rect.bottom < 500:
                    self.rect.y += int(self.vel)
                else:
                    stop_scr()
                    game_over = True
                if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                    self.click = True 
                    mixer.music.load('sfx_swooshing.mp3')
                    mixer.music.set_volume(0.6)
                    mixer.music.play()
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0:
                    self.click = False
                self.image = pygame.transform.rotate(self.images[self.index],self.vel * -2.5)
        else :
            stop_scr()
            if self.rect.bottom < 505:
                self.rect.y += 8
            self.image = pygame.transform.rotate(self.images[self.index],-60)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, point):
        pygame.sprite.Sprite.__init__(self)
        if point == -1:
           image = pygame.transform.flip(image, False, True)
        self.image = image
        self.rect = self.image.get_rect()
        if point == -1 :
            self.rect.bottomleft = [x,y]
        else :
            self.rect.topleft = [x,y]


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        
def draw_scr():
    global bg_scroll,bg_scroll_speed
    for i in range(0,titles + 1):
        screen.blit(bg,(i * (width + 100) + bg_scroll,0))
    bg_scroll -= bg_scroll_speed
    if abs(bg_scroll) == width + 100:
        bg_scroll = 0
def draw_ground():
    global scroll_speed,ground_scroll
    screen.blit(ground,(ground_scroll,500))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) >= 35: 
        ground_scroll = 0

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

bird = Bird(100,height / 2)
bird_group.add(bird)

def count_point():
    global point,pass_pipe
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True 
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right\
            and pass_pipe == True:
            point += 1
            mixer.music.load('sfx_point.mp3')
            mixer.music.play()
            pass_pipe = False
    point_img = font_point.render(str(point), True, white )
    screen.blit(point_img,(300,100))

def show_score():
    global restart
    score = f'Your final sili is {point}'
    score_img = font.render(score,True,white)
    screen.blit(score_img,(180,200))
    screen.blit(restart_img,(230,240))
run = True 
while run :
    clock.tick(fps)
    draw_scr()
    # print(again_rect)
    if flying == False:
        screen.blit(play_txt_img,(200,150))
    if game_over and once:
        mixer.music.load('sfx_die.mp3')
        mixer.music.play()
        once = False
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency and flying == True:
        pipe_height = random.randint(-100,100) + 200
        bottom_pipe = Pipe(width, pipe_height, pipe_img, -1)
        top_pipe = Pipe(width, pipe_height + pipe_gap, pipe_img,1)
        pipe_group.add(bottom_pipe)
        pipe_group.add(top_pipe)
        last_pipe = time_now
    # draw and update
    pipe_group.draw(screen) 
    bird_group.draw(screen)
    pipe_group.update()
    bird_group.update()
    draw_ground()
    if flying == True:
        count_point()
    if game_over:
        show_score()
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True
    # pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True  
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True 
        if event.type == pygame.MOUSEBUTTONUP and clicked == True and game_over == True:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(mouse_pos):
                flying = False
                game_over = False
                once = True  # Reset 'once' to True
                point = 0  # Reset the score
                pass_pipe = False  # Reset the pipe passing flag
                last_pipe = pygame.time.get_ticks()  # Reset the last pipe time

                # Clear the previous sprites from groups
                bird_group.empty()
                pipe_group.empty()

                # Create a new bird and add it to the group
                bird = Bird(100, height / 2)
                bird_group.add(bird)

                # Reset scroll speeds
                bg_scroll_speed = 1
                scroll_speed = 4
    pygame.display.update()
pygame.quit()
sys.exit()