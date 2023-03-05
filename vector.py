import numpy as np
import random

class Vector:
	def __init__(self, x = None, y = None, angle = None, magnitude = None, randomize = False, random_range = [0, 1]):
		self.x = x
		self.y = y
		self.angle = angle
		self.magnitude = magnitude

		if randomize:
			RANGE = random_range[1] - random_range[0]
			self.x = random_range[1] - RANGE*random.random()
			self.y = random_range[1] - RANGE*random.random()
			self.get_magnitude()
			self.get_angle()

		else:
			if x != None and y != None:
				self.get_magnitude()
				self.get_angle()
			else:
				self.calcualte_cart()

	def get_magnitude(self):
		self.magnitude = np.sqrt(self.x**2 + self.y**2)
		return self.magnitude

	def get_angle(self):
		self.angle = np.arctan2(self.y, self.x)
		return self.angle

	def calcualte_cart(self):
		self.x = self.magnitude*np.cos(self.angle)
		self.y = self.magnitude*np.sin(self.angle)

	def add(self, other):
		return Vector(x = self.x + other.x, y = self.y + other.y)

	def zero(self):
		self.x = 0
		self.y = 0
		self.angle = 0
		self.magnitude = 0

	def clamp(self, MIN, MAX):
		new_mag = self.magnitude
		if self.magnitude>MAX:
			new_mag = MAX
		if self.magnitude<MIN:
			new_mag = MIN
		
		if self.magnitude == 0:
			return Vector(x = np.sqrt(new_mag), y = np.sqrt(new_mag))

		x = self.x / self.magnitude*new_mag
		y = self.y / self.magnitude*new_mag

		return Vector(x = x, y = y)

	def normalize(self):
		return Vector(x = self.x/self.magnitude, y = self.y/self.magnitude)

	def rotate(self, angle, degrees = True):
		if degrees:
			angle = angle/180*np.pi
		x = self.x*np.cos(angle)
		y = self.y*np.sin(angle)
		return Vector(x = x, y = y)

	def as_numpy(self):
		return np.array([[self.x, self.y]])

	def __str__(self):
		return f"X: {self.x}, Y: {self.y}, Magnitude: {self.magnitude}, Angle: {self.angle}"

	def __mul__(self, value):
		return Vector(x = self.x*value, y = self.y*value)

	def __add__(self, other):
		return Vector(x = self.x+other.x, y = self.y+other.y)

	def __sub__(self, other):
		return Vector(x = self.x-other.x, y = self.y-other.y)