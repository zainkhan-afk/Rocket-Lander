import numpy as np
from vector import Vector
import config as cfg

class Physics:
	def __init__(self):
		self.gravity = Vector(x = 0, y = 10)

	def collision_det(self, rocket):
		rocket_x1 = rocket.pos.x - cfg.ROCKET_W//2
		rocket_y1 = rocket.pos.y - cfg.ROCKET_H//2
		rocket_x2 = rocket.pos.x + cfg.ROCKET_W//2
		rocket_y2 = rocket.pos.x + cfg.ROCKET_H//2

		if rocket.pos.x<0 or rocket.pos.x>cfg.CANVAS_W:
			rocket.alive = False
			rocket.crashed = True

		if rocket.pos.y<0 or rocket.pos.y>cfg.CANVAS_H:
			rocket.alive = False
			rocket.crashed = True


	def solve(self, rocket):
		rocket.update(self.gravity)
		self.collision_det(rocket)