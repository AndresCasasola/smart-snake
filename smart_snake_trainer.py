###########################################################
#
# - Description: 
#	SmartSnake  is  a  game  where   the   computer   uses 
# 	reinforcement learning to train and learn to play.
#
# - This code is inspired on snakeGame uploaded in github:
#   https://github.com/Bbowen100/SnakeGame.
#
#
# - Author: Andres Casasola Dominguez.
#
###########################################################

# Generic libraries
import sys, pygame, random
import math as m
import numpy as np
import os
# Own libraries
from neuralNet import neural_net
from acsv import csvwrite_acc_loss

############### Definitions
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'smart_snake.h5'
white = 255, 255, 255
font = 200, 200, 200
background = 60, 60, 60
black = 0, 0, 0

class SmartSnake():

############### Init class attributes
	def __init__(self, epochs=10, batch_size=10, epsilon=1, gamma=.8):
		# Neural network attributes
		self.epochs = epochs
		self.batch_size = batch_size
		self.epsilon = epsilon
		self.gamma = gamma
		self.model = neural_net([15, 16])
		self.experience = []
		# Game attributes
		self.width, self.height = 600, 450
		self.score = 0
		self.speed = (0, 0)	# (X, Y)
		self.snake = pygame.image.load("images/snake.png")
		self.snakerect = self.snake.get_rect()
		self.food = pygame.image.load("images/diamond2_res.png")
		self.foodrect = self.food.get_rect()
		self.screen = pygame.display.set_mode([self.width, self.height])

############### End screen
	def end_screen(self):
		self.screen.fill(background)
		endTextSurface = self.gameFont.render('- FINISHED -', 1, font)
		endScoreSurface = self.gameFont.render('Score: ' + str(self.score), 1, font)
		exitButton = pygame.image.load("images/exit_button_black.png")
		exitButtonRect = exitButton.get_rect()
		self.screen.blit(endTextSurface, (self.width/2-(endTextSurface.get_width()/2), self.height/3-(endTextSurface.get_height()/2)))
		self.screen.blit(endScoreSurface, (self.width/2-(endScoreSurface.get_width()/2), self.height/2-(endScoreSurface.get_height()/2)))
		exitButtonRect.move_ip(self.width/2-(exitButtonRect.width/2), self.height/1.2-(exitButtonRect.height/2))
		self.screen.blit(exitButton, exitButtonRect)
		pygame.display.flip()
		# Wait for exit button pressed
		exit = False
		while exit == False:
			pygame.event.wait()
			m1, m2, m3 = pygame.mouse.get_pressed()
			if m1 == True:
				mpos = pygame.mouse.get_pos()
				if exitButtonRect.collidepoint(mpos):
					exit = True

############### Test food collision
	def food_collide(self):
		if self.snakerect.colliderect(self.foodrect):
			return True
		else:
			return False

############### Test frames collision
	def frame_collide(self):
		# Test frame collisions
		if self.snakerect.left < 0 or self.snakerect.right > self.width:
			return True
		if self.snakerect.top < 0 or self.snakerect.bottom > self.height:
			return True
		return False

############### Draw background, snake, food, score and refresh screen
	def draw_screen(self, screen):
		self.screen.fill(background)
		self.screen.blit(self.food, self.foodrect)
		self.screen.blit(self.snake, self.snakerect)
		scoreSurface = self.gameFont.render(str(self.score), 1, font)
		screen.blit(scoreSurface, (30, 30))
		pygame.display.flip()

############### Get current state in the form (snakeX, snakeY, foodX, foodY)
	def get_current_state(self):
		return (self.snakerect.x, self.snakerect.y, self.foodrect.x, self.foodrect.y)

############### Get distance from snake to food
	#def get_distance(self):
		#return m.sqrt(m.pow((self.foodrect.x - self.snakerect.x),2) + m.pow((self.foodrect.y - self.snakerect.y),2))

############### Get distance from snake to food
	def get_distance(self, state):
		return m.sqrt(m.pow((state[2] - state[0]),2) + m.pow((state[3] - state[1]),2))

############### Get the reward for the neural network
	def get_reward(self, last_state, current_state):
		reward = 0
		if self.frame_collide() == True:
			return -50
		last_distance = self.get_distance(last_state)
		current_distance = self.get_distance(current_state)
		if current_distance < last_distance:	# A: If snake is closer to food
			if self.food_collide() == True:	# B: If snake gets the food
				reward = 10	# A
			else:
				reward = 1	# B
		else:	# C: If snake is further to food
			reward = -1	# C
		return reward
			

############### Game main function
	def start_game(self):

		# Init pygame
		pygame.init()

		# Change window name and create gameFont
		pygame.display.set_caption("Smart snake")
		self.gameFont = pygame.font.Font("fonts/comic.ttf", 40)

		## Start position and speed
		snake_start_position = [self.width/5, self.height/2]
		food_start_position = [random.randint(25,self.width-25),random.randint(25,self.height-25)]
		start_speed = (1, 0) # X, Y
		self.snakerect.move_ip(snake_start_position)
		self.foodrect.move_ip(food_start_position)
		speed = start_speed

		## Game variables
		current_state = self.get_current_state()
		last_state = current_state
		
		## Start loop
		run = True
		frame = 0
		action = 0
		while (frame < self.epochs):
			pygame.time.delay(10) # ms
			speed = (0, 0)
			# Capture events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:	# If QUIT event then exit
					print ('Game closed')
					# Save model weights
					if not os.path.isdir(save_dir):
						os.makedirs(save_dir)
					model_path = os.path.join(save_dir, model_name)
					self.model.save(model_path)
					print('Saving trained model at %s ' % model_path)
					sys.exit(0)

			# Decrease epsilon over the first half of training
			if (self.epsilon > 0.1):
				self.epsilon -= (0.9 / self.epochs)

			# Decide which direction the snake will go
			if ((random.random() < self.epsilon) and (frame < self.batch_size)):
				# Take a random direction ['up','down','left','right']
				action = random.choice([0, 1, 2, 3])
				if action == 0: speed = (0, -1)
				if action == 1: speed = (0, 1)
				if action == 2: speed = (-1, 0)
				if action == 3: speed = (1, 0)
				#print('Action:', action)
			else:
				# Get action prediction from the model
				current_state = np.array(self.get_current_state())
				prediction = self.model.predict(np.array([current_state])).flatten().tolist()
				action = prediction.index(max(prediction))
				if action == 0: speed = (0, -1)
				if action == 1: speed = (0, 1)
				if action == 2: speed = (-1, 0)
				if action == 3: speed = (1, 0)
				#print('Prediction: ', np.around(prediction, 2), 'Action: ', action)

			# Save last state
			last_state = current_state
			# Move snake
			self.snakerect = self.snakerect.move(speed)
			# Get current state
			current_state = self.get_current_state()
			# Get reward
			reward = self.get_reward(last_state, current_state)

			# Record experience
			prediction_out = self.model.predict(np.array([last_state])).flatten().tolist()
			prediction_out[action] = reward
			experience = [last_state, prediction_out]
			#print('Experience: ', experience, 'Reward: ', reward)
			self.experience.append(experience)

			# Train neural network
			if(frame == self.batch_size):
				# Get training set from experience
				Xtrain = []
				Ytrain = []
				loss = 0
				for ele in self.experience:
					Xtrain.append(ele[0])
					Ytrain.append(ele[1])

				loss = self.model.fit(np.array(Xtrain), np.array(Ytrain), batch_size=self.batch_size, epochs=self.epochs, verbose = 1)
				# Reset frame and experience
				frame = 0
				self.experience = []

			# Handle collides
			if self.food_collide() == True:
				self.score = self.score + 1		
				self.foodrect.move_ip(random.randint(25,self.width-25)-self.foodrect.x,random.randint(25,self.height-25)-self.foodrect.y)
			if self.frame_collide() == True:
				self.snakerect.move_ip(snake_start_position[0]-self.snakerect.x,snake_start_position[1]-self.snakerect.y)
				self.foodrect.move_ip(random.randint(25,self.width-25)-self.foodrect.x,random.randint(25,self.height-25)-self.foodrect.y)
				self.score = 0

			
			self.draw_screen(self.screen)
			self.get_current_state()
			frame += 1
			## End loop

		
		## Show end screen when game finish
		print(self.experience[0])
		print(self.experience[1])
		print(self.experience[2])
		self.end_screen()


## Understanding the behaviour of the machine learning of this game.
# Playing with epochs and batch_size can be got differents behaviours of the neural network predictions.

# "epochs" are the number of epochs that the neural network trains every time that frame gets the value of batch_size.
# "batch_size" are the number of moves that the game do between every training. For this moves it could use two options:
# 1) An aleatory number got from random() function 
# 2) A prediction from the neural network.
# The selection depends on the epsilon value.

snake = SmartSnake(epochs=10, batch_size=1)
snake.start_game()
pygame.quit()

# Experiments:

# 1) (epochs=10, batch_size=1): At the beginning the snake get closer to the food slowly and very linear, first align with one axis and then with the other.

# 2) (epochs=50, batch_size=10): Minimum loss = 20
