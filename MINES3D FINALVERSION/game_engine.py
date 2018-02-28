from bge import logic
from bge import render
from bge import events
import random
import bge
import fnmatch
import bpy		
#Import der benötigten Module

def Click():	
	#Diese Definition wird im Spiel aufgerufen

	cont = logic.getCurrentController()
	owner = cont.owner
	scene = logic.getCurrentScene()
	Cleared = 0
	mines = 0
	MaxX = 0
	MaxY = 0
	contr = bge.logic.getCurrentController()
	sens = contr.sensors['Message']
	body = sens.subjects

	def setNeighborMine(x,y):
		#Platz neben der ausgewählten Mine festlegen
		lowX = max(x-2, 1)
		highX = min(x+2, 11)
		lowY = max(y-2, 1)
		highY = min(y+2, 11)
		for i in range (lowX, highX): 
			for j in range (lowY, highY):
				if not (i == x and j == y):	#Damit sich das Feld nicht selber mitzählt
					Coord = str(i) + ";" + str(j)
					o = scene.objects[str(Coord)]
					if not o['mine'] == True: #falls das ausgewählte Feld keine Mine ist...
						o['neighborMine'] += 1
						
	def ChangePlate(o, x, y):
		object = str(o)
		if o['neighborMine'] == 1 :
			#Das Feld hat eine Mine in der Nähe
			logic.sendMessage("1","shot",object)	
		elif o['neighborMine'] == 2 :
			#Das Feld hat zwei Minen in der Nähe	
			logic.sendMessage("2","shot",object)
		elif o['neighborMine'] == 3 :
			#Das Feld hat drei Minen in der Nähe
			logic.sendMessage("3","shot",object)		
		elif o['neighborMine'] == 4 :
			#Das Feld hat vier Minen in der Nähe
			logic.sendMessage("4","shot",object)	
		elif o['neighborMine'] == 5 :
			#Das Feld hat fünf Minen in der Nähe			
			logic.sendMessage("5","shot",object)
		elif o['neighborMine'] == 6 :
			#Das Feld hat fünf Minen in der Nähe			
			logic.sendMessage("6","shot",object)
		else : 
			#Das Feld hat keine Mine in der Nähe		
			logic.sendMessage("0","shot",object)
		minenzahl = str(o['neighborMine'])
		print ("Unter der Platte: "+object+" sind/ist "+minenzahl+" Mine/n.")
		
		scene = bge.logic.getCurrentScene()
		cont = bge.logic.getCurrentController()
		own = cont.owner
		obj = scene.objects
		
		x = str(x)
		y = str(y)
		xy = (x+";"+y)
		
		objdel = obj[xy]
		objdel.endObject()	#Ausblenden des Objektes
	
	def Init():
		if not 'init' in owner:
			owner['init'] = 1
			global MaxX
			global MaxY
			global Cleared
			global mines
			Cleared = 0
			MaxX = 10 + 1
			MaxY = 10 + 1
			#Alle Felder auf definieren
			for i in range (1, MaxX):
				for j in range (1, MaxY):
					Coord = str(i) + ";" + str (j)
					o = scene.objects[str(Coord)]
					o['mine'] = False
					o['neighborMine'] = 0
					o['Clicked'] = False
			#10 Minen zufällig setzen
			mines = 10
			for i in range (1, 1 + mines):
				x = random.randrange(1,MaxX)
				y = random.randrange(1,MaxY)
				o = scene.objects[str(x) + ";" + str(y)]
				if o['mine'] == False:
					o['mine'] = True
					i += 1
					setNeighborMine(x,y)
					
	Init()			#------------------ Start ------------------
	def Clicked(x,y):
		global Cleared
		global mines
		Coord = str(x) + ";" + str(y)
		o = scene.objects[str(Coord)]
		if o['Clicked'] == False:			#Gucken ob das Feld schon einmal geöffnet wurde
			if o['mine'] == True:			#falls es noch nicht geöffnet wurde und eine Mine unter der Platte liegt
				print("Game Over")			#Ende vom Spiel und Szenenwechsel 
				scene.replace('GameOver')	#zum GameOver Screen
			elif o['neighborMine'] != 0:	#Wenn es ein benachbartes Feld gibt...
				o['Clicked'] = True
				Cleared += 1
				ChangePlate(o, x, y)
				if mines + Cleared == 100:	#Für den Counter und ob das Feld gelöst wurde
					print(str(Cleared) + " mines cleared! you won!!")
				else:
					print(str(Cleared) + " out of " + str(100-mines) + " cleared, Still " + str(100-mines-Cleared) + " to go")			
			else:							#Wenn das Feld noch nicht geöffnet wurde und es 
				o['Clicked'] = True
				Cleared += 1
				lowX = max(x-1, 1)
				highX = min(x+2, 10)
				lowY = max(y-1, 1)
				highY = min(y+2, 10)
				for i in range (lowX, highX): 
					for j in range (lowY, highY):
							if not (i == x and j == y):
								Coord = str(i) + ";" + str(j)
								o = scene.objects[str(Coord)]
								if o['Clicked'] == False:
									Clicked(i,j)			#Clicked für Nachbarplatten ausführen
	
	if body :								#Wenn die Message, die das Script aufgerufen hat, etwas enthält...
		if not body[0] == "shot" :			#dass nicht "shot" ist
			#print ("Platten Name: ",body[0],"!")
			body = body[0].split(";")
			#print (body)
			x = body[0]
			y = body[1]
			#print ("x: ",x," y: ",y)
			
			Clicked(int(x),int(y))			#dann führe Clicked aus.
			

			

			
			
