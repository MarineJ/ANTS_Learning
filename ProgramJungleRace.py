# coding: utf-8
from math import *
import random, sys, pygame, traceback
from pygame.locals import *
import numpy as np
import pylab as plt


###############################################################
# Global values
###############################################################
pygame.init()
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()
way_1_ants_number = 0
way_2_ants_number = 0
way_3_ants_number = 0
way_4_ants_number = 0

image_ant = pygame.image.load('ant.png').convert()
pygame.transform.scale(image_ant, (32,32))

image_sunny = pygame.image.load('sunny.png').convert()
pygame.transform.scale(image_sunny, (32,32))

image_cloudy = pygame.image.load('cloudy.png').convert()
pygame.transform.scale(image_cloudy, (32,32))

image_rainny = pygame.image.load('rainny.png').convert()
pygame.transform.scale(image_rainny, (32,32))

image_stormy = pygame.image.load('stormy.png').convert()
pygame.transform.scale(image_stormy, (32,32))

weather = 2 # 0 == sunny, 1 == couldy, 2 == rainy, 3 == stormy
nest = []
food = []
road = []

def update_whether():
	print "Changng weather"
	global weather
	weather += 1
	if weather > 3:
		weather = 0
	display_weather()

def display_weather():
	if weather == 0:
		screen.blit(image_sunny,(0,0))
	elif weather == 1:
		screen.blit(image_cloudy,(0,0))
	elif weather == 2:
		screen.blit(image_rainny,(0,0))
	else:
		screen.blit(image_stormy,(0,0))



# pick up one random ant in the nest and one at the food put her on the road
def one_Ant_departure():
	if len(nest) > 0:
		print "Ant departure"
		index_nest = random.randint(0,len(nest)-1)
		nest[index_nest].chose_one_way(0)
	if len(food) > 0:
		index_food = random.randint(0,len(food)-1)
		food[index_food].chose_one_way(1)

def update_all_ants_position():
	if road:
		i=len(road)-1
		while i>0:
			print "Bob"
			road[i].update_position()
			i-=1

###############################################################
# Classe for map
###############################################################

#one of the raceMape
class raceMap(object):
	def __init__(self, water_img, grass_img, road_img, mountain1_img, moutain2_img, moutain3_img, bridge_img):
		"""initializes grid value and load images for texturing the map"""
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

	def displayMap(self):
		"""display the map on the screen once grid values are initialized and texture images are loaded"""
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
		
	def innondations(self):
		"""uptade the map to display a water at the given positions"""
		print "innondation"
		for i in range(4):
			screen.blit(self.water,((13+i)*32,1*32))
		pygame.display.update()

	def predator(self):
		"""update the map to display a predator at the given position"""
		pass

	def melted_tar(self):
		"""update the road to display hard heart on the road"""
		pass

	def tree_on_road(self):
		pass
 
	def trigger_events(self):
		print "trigger_events"
		global weather
		if weather == 0:
			self.melted_tar()
		elif weather == 1:
			self.predator()
		elif weather == 2:
			self.innondations()
		else:
			self.tree_on_road()

###############################################################
# classe for ants
###############################################################

class Ant:
	modelProba = np.ones(4)
	modelProba *= 1./4.;
	def __init__(self, image, x0,y0):
		self.image=image
		self.x = x0
		self.y = y0
		self.previousX = self.x
		self.previousY = self.y
		self.road_number = -1
		self.departure_whether = 0

	def update_position(self):
		print "data"
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
			return
		if tmpx!=self.x or tmpy!=self.y:
			self.previousX = tmpx
			self.previousY = tmpy
		self.display_ant()

	def chose_one_way(self,GorC):
		# random pick a way regarding the model
		# beta = random.random()
		# way_num = 0
		# accu = 0
		# while beta<accu:
		# 	accu+= modelProba[weather,way_num]
		# 	way_num+=1
		way_num=random.randint(GorC,3)
		self.road_number = way_num
		road.append(self)
		nest.remove(self)

		# update number of ants on the give way

		# put the ant on the way
		self.put_ant_on_way(way_num,GorC)
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
				self.x = 26
				self.y = 6
			elif way_num == 1:
				self.x = 25
				self.y = 6
			elif way_num == 2:
				self.x = 25
				self.y = 8
			else:
				self.x = 26
				self.y = 9

	def display_ant(self):
		screen.blit(jungleRaceMap.road,(self.previousY*32,self.previousX*32))  
		screen.blit(image_ant,(self.y*32,self.x*32))

	def chose_one_return_way(self):
		pass

	def update_model(self):
		print "update model"
		pass



###############################################################
# programm
###############################################################


try:
	#create the scene
	jungleRaceMap = raceMap('water.png', 'grass.png', 'road.png', 'mountain1.png', 'moutain2.png', 'moutain3.png', 'bridge.png')
	jungleRaceMap.displayMap()
	display_weather()

	print "Ants creation"
	# create and put all ants in the nest

	for i in range(10):
		nest.append(Ant(image_ant,8,1))


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
		one_Ant_departure()
		jungleRaceMap.trigger_events()
		for i in range(len(road)):
			road[i].update_model()
			pass
		count+=1
		if count == 20:
			update_whether()
			count = 0
		pygame.display.update()
		plt.pause(.5)

except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except:
    print sys.exc_info()[0]
    print traceback.format_exc()

finally:
	pygame.quit()
