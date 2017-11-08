from bge import logic
from bge import render
from bge import events
import random
render.showMouse(True)


def Click():
	
	cont = logic.getCurrentController()
	owner = cont.owner
	scene = logic.getCurrentScene()
	Cleared = 0
	mines = 0
	def setNeighborMine(x,y,z):
		#define area around mine
		lowX = max(x-1, 1)
		highX = min(x+2, 10)
		lowY = max(y-1, 1)
		highY = min(y+2, 10)
		lowZ = max(z-1, 1)
		highZ = min(z+2, 10)
		#loop through area around mine
		for i in range (lowX, highX): 
			for j in range (lowY, highY):
				for k in range (lowZ, highZ):
					#the mine is not a neighbor to itself.
					if not (i == x and j == y and k == z):
						#count neighborMine 1 up for each neighbor
						Coord = str(i) + str(j) + str(k)
						o = scene.objects[str(Coord) + "Cube"]
						#if not neighbor is a mine.
						if not o['mine'] == True: 
							o['neighborMine'] += 1
							#o.color = (1, 0, 0, 1)
	
	def ColorSphere(o):
		if o['neighborMine'] == 1 :
			o.color = (0,1,0,1)			#Green
		elif o['neighborMine'] == 2 :
			o.color = (1,1,0,1)			#Yellow
		elif o['neighborMine'] == 3 :
			o.color = (1,0,0,1)			#Red
		elif o['neighborMine'] == 4 :
			o.color = (1,0,1,1)			#Magenta
		elif o['neighborMine'] == 5 :
			o.color = (0,0,1,1)			#Blue
		else : 
			o.color = (1,1,1,1)			#White
	def Init():
		if not 'init' in owner:
			owner['init'] = 1
			global Cleared
			global mines
			Cleared = 0
			#loop through all spheres and set there mine status to False
			for i in range (1, 10): 
				for j in range (1, 10):
					for k in range (1, 10):
						Coord = str(i) + str(j) + str(k)
						o = scene.objects[str(Coord) + "Cube"]
						o['mine'] = False
						o['neighborMine'] = 0
			# set 10 random spheres to be mines.
			mines = 10
			for i in range (1, 1 + mines):
				x = random.randrange(1,10)
				y = random.randrange(1,10)
				z = random.randrange(1,10)
				o = scene.objects[str(x) + str(y) + str(z) + "Cube"]
				if o['mine'] == False:
					o['mine'] = True
					#o.color = (0, 0, 0, 1)
					i += 1
					setNeighborMine(x,y,z)
	Init()
	def Clicked(x,y,z):
		global Cleared
		global mines
		Coord = str(x) + str(y) + str(z)
		o = scene.objects[str(Coord) + "Cube"]
		if o['Clicked'] == False:
			if o['mine'] == True:
				print("Game Over")
				#code to end game here!
			elif o['neighborMine'] != 0:
				o['Clicked'] = True
				Cleared += 1
				ColorSphere(o)
				#o.color = (0, 1, 0, 1)
				if mines + Cleared == 729:
					print(str(Cleared) + " mines cleared! you won!!")
				else:
					print(str(Cleared) + " out of " + str(729-mines) + " cleared, Still " + str(729-mines-Cleared) + " to go")			
			else :
				o['Clicked'] = True
				Cleared += 1
				o.visible = False
				o.occlusion = False
				#define area around click
				lowX = max(x-1, 1)
				highX = min(x+2, 10)
				lowY = max(y-1, 1)
				highY = min(y+2, 10)
				lowZ = max(z-1, 1)
				highZ = min(z+2, 10)
				#loop through area around click
				for i in range (lowX, highX): 
					for j in range (lowY, highY):
						for k in range (lowZ, highZ):
							#dont click itself
							if not (i == x and j == y and k == z):
								Coord = str(i) + str(j) + str(k)
								o = scene.objects[str(Coord) + "Cube"]
								if o['Clicked'] == False:
									Clicked(i,j,k)
	MouseOver = cont.sensors["MouseOver"]
	ob = MouseOver.hitObject
	MouseLeft = cont.sensors["MouseLeft"]
	if MouseLeft.positive and ob != None:
		loc = str(ob)[:3]
		x = loc[:1]
		y = loc[1:2]
		z = loc[2:3]
		Clicked(int(x),int(y),int(z))
		#print("x=" +x+", y="+y+", z="+z)
		return(x,y,z)

