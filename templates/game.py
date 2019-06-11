
import sys, pygame

pygame.init()

size = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My first game")

run = True

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.ESC:
			run = False

pygame.quit()
