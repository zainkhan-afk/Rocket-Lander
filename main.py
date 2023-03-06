from renderer import Renderer
from rocket import Rocket
from physics import Physics
from controller import Controller
import numpy as np

renderer = Renderer()
rocket = Rocket()
physics = Physics()

my_controller = Controller()
rocket.connect_controller(my_controller)
while True:
	physics.solve(rocket)
	renderer.clear()
	renderer.draw(rocket)
	k = renderer.render()

	if k == ord("q"):
		break

	elif k == ord("d"):
		my_controller.angle += 5/180*np.pi
		# my_controller.angle = 45/180*np.pi

	elif k == ord("a"):
		my_controller.angle -= 5/180*np.pi
		# my_controller.angle = -45/180*np.pi


	elif k == ord("w"):
		my_controller.magnitude -= 0.5

	elif k == ord("s"):
		my_controller.magnitude += 0.5

	elif k == ord(" "):
		my_controller.magnitude = -100

	else:
		my_controller.magnitude = -1
		# my_controller.angle = 0