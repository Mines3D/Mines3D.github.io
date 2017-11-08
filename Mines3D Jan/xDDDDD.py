from bge import logic
from bge import render
from bge import events
import random

def Click():

	cont = logic.getCurrentController()
	owner = cont.owner
	scene = logic.getCurrentScene()
	Cleared = 0
	mines = 0
	
	def setNeighborMine(x,y):
		#Platz neben Minen
		lowX = max(x-1, 1)
		highX = min(x+2, 10)
		lowY = max(y-4, 1)
		highY = min(y+2, 10)
		for i in range (lowX, highX): 
			for j in range (lowY, highY)
				if not (i == x and j == y):	#Der Nachbar ist nicht die Mine
					Coord = str(i) + str(j) + str(x)
					o = scene.objects[str(Coord) + "Cube"]
					if not o['mine'] == True: #falls Nachbar keine Mine ist...
						o['neighborMine'] += 1
	
	def ColorSphere(o):
		if o['neighborMine'] == 1 :
			number = 1			#Green
		elif o['neighborMine'] == 2 :
			number = 2			#Yellow
		elif o['neighborMine'] == 3 :
			number = 3			#Red
		elif o['neighborMine'] == 4 :
			number = 4			#Magenta
		elif o['neighborMine'] == 5 :
			number = 5			#Blue
		else : 
			number = 0			#White
	
	def Init():
		if not 'init' in owner:
			owner['init'] = 1
			global Cleared
			global mines
			Cleared = 0
			#Alle Felder auf "keine Mine" setzen
			for i in range (1,10):
				for j in range (1, 10):
					Coord = str(i) + str (j)
					o = scene.objects[str(Coord) + "Cube"]
					o['mine'] = False
					o['neighborMine'] = 0
			#Minen zufällig setzen
			mines = 10
			for i in range (1, 1 + mines):
				x = random.randrange(1,10)
				y = random.randrange(1,10)
				o = scene.objects[str(x) + str(y) + "Cube"]
				if o['mine'] == False:
					o['mine'] = True
					i += 1
					setNeighborMine(x,y)
	Init()
	def Clicked(x,y)
		global Cleared
		global mines
		Coord = str(x) + str(y)
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
				if mines + Cleared == 100:
					print(str(Cleared) + " mines cleared! you won!!")
				else:
					print(str(Cleared) + " out of " + str(100-mines) + " cleared, Still " + str(100-mines-Cleared) + " to go")			
	
	#Rausgelassen 
		
			# else :
				# o['Clicked'] = True
				# Cleared += 1
				# o.visible = False
				# o.occlusion = False
				##define area around click
				# lowX = max(x-1, 1)
				# highX = min(x+2, 10)
				# lowY = max(y-1, 1)
				# highY = min(y+2, 10)
				##loop through area around click
				# for i in range (lowX, highX): 
					# for j in range (lowY, highY):
							##dont click itself
							# if not (i == x and j == y):
								# Coord = str(i) + str(j)
								# o = scene.objects[str(Coord) + "Cube"]
								# if o['Clicked'] == False:
									# Clicked(i,j)
	
	
	
	#Zu bearbeiten:
		 MouseOver = cont.sensors["MouseOver"]
		 ob = MouseOver.hitObject
		 MouseLeft = cont.sensors["MouseLeft"]
		 if MouseLeft.positive and ob != None:
			 loc = str(ob)[:3]
			 x = loc[:1]
			 y = loc[1:2]
			 Clicked(int(x),int(y))
			#print("x=" +x+", y="+y+", z="+z)
			 return(x,y)