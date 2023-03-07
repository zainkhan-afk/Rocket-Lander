from vector import Vector
import config as cfg
import numpy as np
from utils import *

class Controller:
	def __init__(self):
		self.t = 0

		self.angle = 0
		self.magnitude = -9.8

	def get_force_vectors(self, control_vector):
		mag1 = control_vector[0, 0]*cfg.THRUSTER_MAGNITUDE_MAX
		ang1 = control_vector[1, 0]*np.pi/2
		mag2 = control_vector[2, 0]*cfg.THRUSTER_MAGNITUDE_MAX
		ang2 = control_vector[3, 0]*np.pi/2

		left_thruster  = Vector(magnitude = mag1, angle = np.pi/2 + ang1)
		right_thruster = Vector(magnitude = mag2, angle = np.pi/2 + ang2)

		# left_thruster  = Vector(magnitude = -20, angle = np.pi/2 )
		# right_thruster = Vector(magnitude = -20, angle = np.pi/2 )

		self.t += cfg.DELTA_T

		return left_thruster, right_thruster