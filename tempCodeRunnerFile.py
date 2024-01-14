# import pygame and sys 
import pygame 
import sys 

from pygame.locals import *

# pygame.init() will initialize all 
# imported module 
pygame.init() 
pygame.display.set_caption('GeeksforGeeks') 

# screen size will display on screen 
screen = pygame.display.set_mode((600, 700), 0, 32) 

# pygame.image.load() will return the 
# object that has image 
img = pygame.image.load('pipe.png') 

while True: 
	
	# Background color 
	screen.fill((255, 255, 255)) 
	
	# image copy 
	img_copy = img.copy() 
	
	# pygame.transform.flip() will flip the image 
	img_with_flip = pygame.transform.flip(img_copy, False, True) 
	
	# surface.blit() function draws a source 
	# Surface onto this Surface. 
	screen.blit(img_with_flip, (50 + 1 * 120, 100)) 
	
	# event listener to quit screen 
	for event in pygame.event.get(): 
		if event.type == QUIT: 
			pygame.quit() 
			sys.exit() 

	# update the frame per second 
	pygame.display.update() 
