from renderer import Renderer
from physics import Physics
import numpy as np
import config as cfg


class Simulator:
	def __init__(self, headless = False):
		self.renderer = Renderer()
		self.physics = Physics()
		self.headless = headless
		self.t = 0


	def step(self, all_entities):
		self.renderer.clear()
		for i, entity in enumerate(all_entities):
			if entity.alive:
				self.physics.solve(entity)
				if not self.headless:
					self.renderer.draw(entity)

			if entity.age>500:
				entity.alive = False

		self.t += cfg.DELTA_T
		
		k = ' '
		if not self.headless:
			k = self.renderer.render()
		return k

		# if k == ord("q"):
		# 	break