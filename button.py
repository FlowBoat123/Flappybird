import pygame,sys 
pygame.init()

#set up screen
scr_col = (50,200,200)
width = 500
height = 500
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("buttonext")

#set up clock and font 
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,40)

class initialize():
    def __init__(self,width,height,pos,text,elevation):
            self.clicked = False
            self.elevation = elevation
            self.dynamic_elevation = elevation
            self.original_y_pos = pos[1]
            # top rect
            self.top_rect = pygame.Rect(pos,(width,height))
            self.top_color = '#475F77'
            #bottom rect
            self.bot_rect = pygame.Rect(pos,(width,elevation))
            self.bot_color = '#354B5E'
            # text
            self.text_surf = font.render(text,True,'#FFFFFF')
            self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bot_rect.midtop = self.top_rect.midtop
        self.bot_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen,self.bot_color,self.bot_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color,self.top_rect,border_radius = 12)
        screen.blit(self.text_surf,self.text_rect)
    def check_click(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#BD072C'
            self.dynamic_elevation = 0
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True 
                action = True
            else :
                if self.clicked == True:
                    #print("click")
                    self.clicked = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'
        return action
