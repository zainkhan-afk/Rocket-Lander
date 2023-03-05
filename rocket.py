from vector import Vector
import config as cfg
import numpy as np
from utils import *
from controller import Controller

class Rocket:
	def __init__(self, controller = None):
		self.controller = controller

		self.pos = Vector(x = cfg.CANVAS_W//2, y = cfg.CANVAS_H//2)
		self.vel = Vector(x = 0, y = 0)
		self.orientation = 0
		self.thruster_dist = 40

		self.left_thruster_pos_relative  = np.array([[-self.thruster_dist, 0]])
		self.right_thruster_pos_relative = np.array([[ self.thruster_dist, 0]])

		self.left_thruster_pos  = get_transformed_pts(self.left_thruster_pos_relative, self.orientation, self.pos)
		self.right_thruster_pos = get_transformed_pts(self.right_thruster_pos_relative, self.orientation, self.pos)

		self.thruster_left_force_world_frame = Vector(x = 0, y =  1)
		self.thruster_right_force_world_frame = Vector(x = 0, y = 1)

		self.color = (255, 0, 0)
		self.thruster_color = (0, 255, 255)
		self.fire_color = (0, 0, 255)
		self.lander_color = (125, 125, 125)
		self.top_color = (0, 0, 255)

		self.mass = 1
		self.rocket_w = 30
		self.rocket_h = 15

		self.tail = np.array([[self.pos.x, self.pos.y]])

	def connect_controller(self, controller):
		self.controller = controller


	def update(self, acc):
		if self.controller is not None:
			thruster_left_force_robot_frame, thruster_right_force_robot_frame = self.controller.get_force_vectors()
			self.thruster_left_force_world_frame  = get_transformed_vector(thruster_left_force_robot_frame, self.orientation)
			self.thruster_right_force_world_frame = get_transformed_vector(thruster_right_force_robot_frame, self.orientation)

			net_torque = thruster_right_force_robot_frame.y*self.thruster_dist - thruster_left_force_robot_frame.y*self.thruster_dist
			angular_acc = net_torque/(self.thruster_dist*self.mass)

			self.orientation += angular_acc*(cfg.DELTA_T**2)

		left_thruster_acc  = self.thruster_left_force_world_frame *(1/(self.mass*2))
		right_thruster_acc = self.thruster_right_force_world_frame*(1/(self.mass*2))
		thrust_acc = left_thruster_acc + right_thruster_acc		
		# thrust_acc = net_thrust_force*(1/self.mass)


		self.tail =np.append(self.tail, np.array([[self.pos.x, self.pos.y]]), axis = 0)

		net_acc = acc+thrust_acc

		self.vel += net_acc*cfg.DELTA_T

		self.vel.clamp(-10, 10)

		self.pos += self.vel*cfg.DELTA_T

		self.left_thruster_pos  = get_transformed_pts(self.left_thruster_pos_relative, self.orientation, self.pos)
		self.right_thruster_pos = get_transformed_pts(self.right_thruster_pos_relative, self.orientation, self.pos)


		if self.pos.x>cfg.CANVAS_W:
			self.pos.x = 0

		elif self.pos.x<0:
			self.pos.x = cfg.CANVAS_W

		if self.pos.y>cfg.CANVAS_H:
			self.pos.y = 0

		elif self.pos.y<0:
			self.pos.y = cfg.CANVAS_H