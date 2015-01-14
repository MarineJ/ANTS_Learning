# coding: utf-8
from math import *
import random, sys, pygame
from pygame.locals import *
import numpy as np
import pylab as plt


###############################################################
# Global values
###############################################################
pygame.init()
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()
way_1_ants_number = 0.
way_2_ants_number = 0.
way_3_ants_number = 0.
way_4_ants_number = 0.

whether = "sunny"
nest = []
food = []
road = []

def upadta_whether():
	if whether == "sunny":
		whether = "cloudy"
	elif whether == "cloudy":
		whether = "rainy"
	elif whether == "rainy":
		whether = "stormy"
	else:
		whether = "sunny"

# pick up one random ant in the nest and one at the food put her on the road
def one_Ant_departure():
	index_nest = random.random()*nest.amount()
	index_food = random.random()*food.amount()
	nest(index_nest).chose_one_way()
	food(index_food).chose_on_return_way()



###############################################################
# Classe for map
###############################################################

#one of the raceMape
class raceMap(object):
     
    raceMapGrid = []

    # initializes grid value and load images for texturing the map 
    def __init__(self, water_img, grass_img, road_img, mountain1_img, moutain2_img, moutain3_img, bridge_img):
    	self.water = pygame.image.load(water_img).convert()
    	pygame.transform.scale(self.water, (32,32))
    	self.road = pygame.image.load(road_img).convert()
    	pygame.transform.scale(self.road, (32,32))
    	self.grass = pygame.image.load(grass_img).convert()
    	pygame.transform.scale(self.grass, (32,32))
    	self.raceMapGrid = np.matrix([
    		   [0., 1., 1., 1.,1., 1., 1., 1., 1., 1., 4., 1., 2., 2., 2., 2., 2., 2., 2., 2., 2, 2., 2., 2., 2, 2., 2., 10.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1.,1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]])

    # display the map on the screen once grid values are initialized and texture images are loaded
    def displayMap(self):
    	for i in range(20):
    		for j in range(18):
				if self.raceMapGrid[i,j]==1.:
					screen.blit(self.water,(i*32,j*32))
				elif self.raceMapGrid[i,j]==0.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==2.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==4.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==5.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==6.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==7.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==8.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==9.:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[i,j]==10.:
					screen.blit(self.grass,(i*32,j*32))
		pygame.display.update()
		
	# uptade the map to display a water at the given positions
	def innondations(self):
		pass

	# update the map to display a predator at the given position
	def predator(self):
		pass
	# update the road to display hard heart on the road
	def melted_tar(self):
		pass
	# 
	def trigger_events(self):
		pass

###############################################################
# classe for rats
###############################################################

class Ant:

	modelProba = np.full((4,4),1./4.)

	def _init_(self, image, position):
		self.image = pygame.load.image(image)
		self.x = position[0]
		self.y = position[1]
		self.previousX = self.x
		self.previousY = self.y
		self.departure_whether = "sunny"
		


	def update_position(self, movement):
		self.previousX = self.x
		self.previousY = self.y
		if (self.x+movement[0])>0 and (self.x+movement[0])<28:
			self.x += movement[0]
		if (self.y+movement[1])>0 and (self.y+movement[1])<20:
			self.y += movement[1]

	
	def chose_one_way():
		pass

	def chose_one_return_way():
		pass

	def update_model():
		pass










###############################################################
# programm
###############################################################


try:
	#create the scene
	jungleRaceMap = raceMap('water.png', 'grass.png', 'road.png', 'mountain1.png', 'moutain2.png', 'moutain3.png', 'bridge.png')
	print(jungleRaceMap)
	jungleRaceMap.displayMap()

	# ask user to put goals on the map

	# display map , goals and rat and run simulation

	# user input and simulation runing
	deltat = clock.tick(30)
	while 1:
		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			down = event.type == KEYDOWN
			if event.key == K_RIGHT: print('right')
			elif event.key == K_LEFT: print('left')
			elif event.key == K_UP: print('up')
			elif event.key == K_DOWN: print('down')
			elif event.key == K_ESCAPE: 
				pygame.quit()
				sys.exit()
	pygame.display.update()

finally:
	pygame.quit()
	sys.exit()
