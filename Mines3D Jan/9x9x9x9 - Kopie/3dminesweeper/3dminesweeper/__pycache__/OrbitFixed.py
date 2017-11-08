from bge import logic
from bge import events
from bge import render

def Camera():
	cont = logic.getCurrentController()
	obj = cont.owner

	mouse = logic.mouse

	mmb = events.MIDDLEMOUSE

	winw = render.getWindowWidth()
	winh = render.getWindowHeight()

	spd = 2.0 # How fast to rotate the view

	minimum = 0.002  # How little you have to move the mouse to rotate the view (eliminates drifting)

	if not 'init' in obj:
		obj['init'] = 1
		obj['set'] = 0
		obj['prevpos'] = [0, 0]

	if mouse.events[mmb] and obj['set']:
		
		render.setMousePosition(int(winw / 2), int(winh / 2))
		
		mx = mouse.position[0] - 0.5
		my = mouse.position[1] - 0.5 
		
		if abs(mx) > minimum:
			
			obj.applyRotation([0.0, 0.0, mx * spd], 0)
			
		if abs(my) > minimum:
		
			obj.applyRotation([my * spd, 0.0, 0.0], 1)
			
	if mouse.events[mmb] == 1:
		
		render.setMousePosition(int(winw / 2), int(winh / 2))
		
		obj['set'] = 1
			
	if mouse.events[mmb] == 3:
		obj['set'] = 0
		render.setMousePosition(obj['prevpos'][0], obj['prevpos'][1])
		#print (obj['prevpos'])

	if not mouse.events[mmb]:
		obj['prevpos'] = int(mouse.position[0] * winw), int(mouse.position[1] * winh)