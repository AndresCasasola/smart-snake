
import sys, pygame, random

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# Start mixer with 22050Hz, 2 channels, 16 bit sample size
# Init mixer before pygame, otherwise the buffer does not assign right
pygame.mixer.init(frequency=48000, channels=2, size=16, buffer=512)#22050
# Init pygame
pygame.init()
############### Init environment
# Show 800x600 window
width, height = 600, 450
screen = pygame.display.set_mode([width, height])
s_score = pygame.mixer.Sound("sounds/TP_Get_Rupee.wav")
s_hit = pygame.mixer.Sound("sounds/HitSound.wav")
# Change window name
pygame.display.set_caption("Travieso snake")
gameFont = pygame.font.Font("fonts/comic.ttf", 40)
#gameFont = pygame.font.SysFont("Comic Sans", 40)
############### Variables
snake_start_position = [width/5, height/2]
food_start_position = [random.randint(25,width-25),random.randint(25,height-25)]
start_speed = [1, 0] # X, Y
score=0;
speed = start_speed
snake = pygame.image.load("images/snake.png")
snakerect = snake.get_rect()
food = pygame.image.load("images/diamond2_res.png")
foodrect = food.get_rect()
# Colors
white = 255, 255, 255
font = 200, 200, 200
background = 60, 60, 60
black = 0, 0, 0

# Start position
snakerect.move_ip(snake_start_position)
last = foodrect.move_ip(food_start_position)

############### Loop conditions
run = True
stop = False
############### Start loop
while run:
	if stop == True:
		pygame.time.delay(1*1000) # ms
	
	pygame.time.delay(5) # ms
	# Capture events
	for event in pygame.event.get():
		# If QUIT event then exit
		if event.type == pygame.QUIT: run = False
############### Key events
	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
		speed = [0, 0]
	if keys[pygame.K_UP]:
		speed[1] = -1;
	if keys[pygame.K_DOWN]:
		speed[1] = 1;
	if keys[pygame.K_LEFT]:
		speed[0] = -1;
	if keys[pygame.K_RIGHT]:
		speed[0] = 1;
	if keys[pygame.K_p]:
		if stop == True:
			stop = False
			
############### Test colission
	if snakerect.colliderect(foodrect):
		if colliding == False:
			score = score + 1;			
			s_score.play()
			#s_hit.play()
			foodrect.move_ip(random.randint(25,width-25)-foodrect.x,random.randint(25,height-25)-foodrect.y)
			colliding = True
	else:
		colliding = False

	# Move snake
	snakerect = snakerect.move(speed)

	if snakerect.left < 0 or snakerect.right > width:
		run = False
	if snakerect.top < 0 or snakerect.bottom > height:
		run = False

############### Draw background, snake, food, score and refresh screen
	screen.fill(background)
	screen.blit(food, foodrect)
	screen.blit(snake, snakerect)
	scoreSurface = gameFont.render(str(score), 1, font)
	screen.blit(scoreSurface, (30, 30))
	pygame.display.flip()

############### End screen
screen.fill(background)
endTextSurface = gameFont.render('- YOU DIED -', 1, font)
endScoreSurface = gameFont.render('Score: ' + str(score), 1, font)
exitButton = pygame.image.load("images/exit_button_black.png")
exitButtonRect = exitButton.get_rect()
screen.blit(endTextSurface, (width/2-(endTextSurface.get_width()/2), height/3-(endTextSurface.get_height()/2)))
screen.blit(endScoreSurface, (width/2-(endScoreSurface.get_width()/2), height/2-(endScoreSurface.get_height()/2)))
exitButtonRect.move_ip(width/2-(exitButtonRect.width/2), height/1.2-(exitButtonRect.height/2))
screen.blit(exitButton, exitButtonRect)
pygame.display.flip()

exit = False
while exit == False:
	pygame.event.wait()
	m1, m2, m3 = pygame.mouse.get_pressed()
	if m1 == True:
		mpos = pygame.mouse.get_pos()
		if exitButtonRect.collidepoint(mpos):
			exit = True

#pygame.time.delay(2*1000) # ms

pygame.quit()


