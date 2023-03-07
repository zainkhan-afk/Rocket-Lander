from simulator import Simulator
from rocket import Rocket
from controller import Controller
import numpy as np

sim = Simulator()

all_entities = []
rocket = Rocket()
my_controller = Controller()
rocket.connect_controller(my_controller)

all_entities.append(rocket)
while True:
	k = sim.run_step(all_entities)

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