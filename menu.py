import pygame,sys 
import button 
pygame.init()

# Set up some constants...
width = 540
height = 540
screen = pygame.display.set_mode((width,height))

#set some color, font and clock
scr_col = '#532DC7'
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,40)

#Set button play
play_text = "Play"
play_button = button.initialize(150,50,(200,150),play_text,6)
option_text = "Option"
option_button = button.initialize(150,50,(200,250),option_text,6)
exit_text = "Quit"
exit_button = button.initialize(150,50,(200,350),exit_text,6)

run = True
def draw_scr():
    global run
    screen.fill(scr_col)
    play_button.draw()
    option_button.draw()
    exit_button.draw()
    play_button.check_click()
    option_button.check_click()
    if exit_button.check_click():
        run = False

while run :
    draw_scr()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()