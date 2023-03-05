from vector import Vector
import config as cfg
import numpy as np
from utils import *

class Controller:
	def __init__(self):
		self.t = 0

		self.angle = 0
		self.magnitude = -9.8

	def get_force_vectors(self):
		left_thruster  = Vector(magnitude = self.magnitude, angle = np.pi/2 + self.angle)
		right_thruster = Vector(magnitude = self.magnitude, angle = np.pi/2 + self.angle)


		# left_thruster  = Vector(magnitude = self.magnitude + np.random.normal(), angle = np.pi/2 + np.random.normal()*0.05)
		# right_thruster = Vector(magnitude = self.magnitude + np.random.normal(), angle = np.pi/2 + np.random.normal()*0.05)

		self.t += cfg.DELTA_T

		return left_thruster, right_thruster