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

weather = 2 # 0 == sunny, 1 == couldy, 2 == rainy, 3 == stormy
nest = []
food = []
road = []

def update_whether():
	print "Changng weather"
	global weather
	weather += 1
	if weather > 4:
		weather = 0

# pick up one random ant in the nest and one at the food put her on the road
def one_Ant_departure():
	if len(nest) > 0:
		print "Ant departure"
		index_nest = random.randint(0,len(nest)-1)
		nest[index_nest].chose_one_way()
	# if len(food) > 0:
		# index_food = random.randint(0,len(food)-1)
		# food[index_food].chose_on_return_way()

def update_all_ants_position():
	if road:
		for i in range(len(road)):
			if road[i].update_position()==1:
				print "one in food", i, i-1
				i-=1
				print road[i]





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
    		   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1],
               [1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1],
               [1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1],
               [1, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 1],
               [2, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 3, 3, 3, 8, 8],
               [2, 2, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8],
               [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8],
               [2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 8, 8],
               [3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1],
               [3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 1],
               [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
               [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
               [1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 1],
               [1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

    # display the map on the screen once grid values are initialized and texture images are loaded
    def displayMap(self):
    	for i in range(28):
    		for j in range(19):
				if self.raceMapGrid[j,i]==1:
					screen.blit(self.grass,(i*32,j*32))
				elif self.raceMapGrid[j,i]==2 or self.raceMapGrid[j,i]==8:
					screen.blit(self.road,(i*32,j*32))
				elif self.raceMapGrid[j,i]==3:
					screen.blit(self.road,(i*32,j*32))
				else:
					print "unknow value"
				#elif self.raceMapGrid[j,i]==4.:
					#screen.blit(self.water,(i*32,j*32))
		pygame.display.update()
		
	# uptade the map to display a water at the given positions
	def innondations(self):
		print "innondation"
		for i in range(4):
			screen.blit(self.water,((13+i)*32,1*32))
		pygame.display.update()


	# update the map to display a predator at the given position
	def predator(self):
		pass

	# update the road to display hard heart on the road
	def melted_tar(self):
		pass

	def tree_on_road(self):
		pass
 
	def trigger_events(self):
		print "trigger_events"
		global weather
		if weather == 0:
			melted_tar()
		elif weather == 1:
			predator()
		elif weather == 2:
			innondations()
		else:
			tree_on_road()

###############################################################
# classe for ants
###############################################################

class Ant:

	modelProba = np.full((4,4),1./4.)

	def __init__(self, image, x0,y0):
		self.image=image
		self.x = x0
		self.y = y0
		self.previousX = self.x
		self.previousY = self.y
		self.road_number = -1
		self.departure_whether = 0

		


	def update_position(self):
		tmpx = self.x	
		tmpy = self.y
		if jungleRaceMap.raceMapGrid[self.x-1, self.y]==3 and self.x-1 != self.previousX and tmpx!=0:
			self.x-=1
		elif jungleRaceMap.raceMapGrid[self.x+1, self.y]==3 and self.x+1 != self.previousX and tmpx!=19:
			self.x+=1
		elif jungleRaceMap.raceMapGrid[self.x, self.y-1]==3 and self.y-1 != self.previousY and tmpy!=0:
			self.y-=1
		elif jungleRaceMap.raceMapGrid[self.x, self.y+1]==3 and self.y+1 != self.previousY and tmpy!=27:
			self.y+=1 
		else: # sinon on est arrivé
			food.append(self)
			road.remove(self)
			print "arrive in food", len(food)
			return 1
		self.previousX = tmpx
		self.previousY = tmpy
		self.display_ant()
		return 0
	
	def chose_one_way(self):
		# random pick a way regarding the model
		# beta = random.random()
		# way_num = 0
		# accu = 0
		# while beta<accu:
		# 	accu+= modelProba[weather,way_num]
		# 	way_num+=1
		way_num=random.randint(0,3)
		self.road_number = way_num
		road.append(self)
		nest.remove(self)

		# update number of ants on the give way

		# put the ant on the way
		self.put_ant_on_way(way_num,0)
		self.display_ant()


	def put_ant_on_way(self, way_num, GorC):
		if GorC == 0:
			if way_num == 0:
				self.x = 6
				self.y = 1
			elif way_num == 1:
				self.x = 8
				self.y = 2
			elif way_num == 2:
				self.x = 10
				self.y = 2
			else:
				self.x = 11
				self.y = 0
		else:
			if way_num == 0:
				self.x = 0
				self.y = 0
			elif way_num == 1:
				self.x = 0
				self.y = 0
			elif way_num == 2:
				self.x = 0
				self.y = 0
			else:
				self.x = 0
				self.y = 0



	def display_ant(self):
		screen.blit(jungleRaceMap.road,(self.previousY*32,self.previousX*32))  
		screen.blit(jungleRaceMap.water,(self.y*32,self.x*32))


	def chose_one_return_way():
		pass

	def update_model():
		print "update model"
		pass



###############################################################
# programm
###############################################################


try:
	#create the scene
	jungleRaceMap = raceMap('water.png', 'grass.png', 'road.png', 'mountain1.png', 'moutain2.png', 'moutain3.png', 'bridge.png')
	jungleRaceMap.displayMap()

	print "Ants creation"
	# create and put all ants in the nest
	image = pygame.image.load('rat.png').convert()
	pygame.transform.scale(image, (32,32))
	for i in range(10):
		nest.append(Ant(image,8,1))


	# user input and simulation runing
	deltat = clock.tick(30)
	count = 0
	print "Start simulation"
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
		update_all_ants_position()
		print "bob"
		one_Ant_departure()
		#jungleRaceMap.trigger_events()
		for i in range(len(road)):
			#road[i].update_model()
			pass
		count+=1
		if count == 20:
			update_whether()
			count = 0
		pygame.display.update()
		plt.pause(.5)

finally:
	pygame.quit()
	sys.exit()
