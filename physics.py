import numpy as np
from vector import Vector

class Physics:
	def __init__(self):
		self.gravity = Vector(x = 0, y = 9.8)

	def solve(self, rocket):
		rocket.update(self.gravity)