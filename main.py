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

	if k == ord("d"):
		my_controller.angle += 5/180*np.pi

	if k == ord("a"):
		my_controller.angle -= 5/180*np.pi


	if k == ord("w"):
		my_controller.magnitude -= 0.5

	if k == ord("s"):
		my_controller.magnitude += 0.5