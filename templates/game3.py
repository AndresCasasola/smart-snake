
import sys, pygame

# Init pygame
pygame.init()
# Show 800x600 window
size = 800, 600
screen = pygame.display.set_mode(size)
# Start mixer with 22050Hz, 2 channels, 16 bit sample size
pygame.mixer.init(frequency=22050, channels=1, size=16, buffer=4096)
s = pygame.mixer.Sound("./sounds/TP_Secret.wav")

# Cambio el título de la ventana
pygame.display.set_caption("Ballgame")
# Inicializamos variables
width, height = 800, 600
speed = [1, 1]
white = 255, 255, 255
# Crea un objeto imagen pelota y obtengo su rectángulo
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()
# Crea un objeto imagen bate y obtengo su rectángulo
bate = pygame.image.load("bate.png")
baterect = bate.get_rect()
# Pongo el bate en el centro de la pantalla
baterect.move_ip(500, 300)
# Comenzamos el bucle del juego
run=True
while run:
	# Espero un tiempo (milisegundos) para que la pelota no vaya muy rápida
	pygame.time.delay(0)
	# Capturamos los eventos que se han producido
	for event in pygame.event.get():
		#Si el evento es salir de la ventana, terminamos
		if event.type == pygame.QUIT: run = False
	# Compruebo si se ha pulsado alguna tecla
	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP]:
		baterect=baterect.move(0, -1)
	if keys[pygame.K_DOWN]:
		baterect=baterect.move(0, 1)
	if keys[pygame.K_LEFT]:
		baterect=baterect.move(-1, 0)
	if keys[pygame.K_RIGHT]:
#		baterect=baterect.move(1, 0)
		s.play(loops=0)
	# Compruebo si hay colisión
	if baterect.colliderect(ballrect):
		speed[0] = - speed[0]
	# Muevo la pelota
	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]
	#Pinto el fondo de blanco, dibujo la pelota/bate y actualizo la pantalla
	screen.fill(white)
	screen.blit(ball, ballrect)
	screen.blit(bate, baterect)
	pygame.display.flip()
# Salgo de pygame
pygame.quit()
