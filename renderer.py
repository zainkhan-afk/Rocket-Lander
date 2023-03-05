import cv2
import numpy as np
import config as cfg
from utils import *

class Renderer:
	def __init__(self):
		self.canvas = np.zeros((cfg.CANVAS_H, cfg.CANVAS_W, 3)).astype("uint8")
		self.rocket_body = np.array([
								[-30, -15],
								[ 30, -15],
								[ 30,  15],
								[-30,  15]
									])

		self.rocket_top = np.array([
								[-30, -17],
								[ 0,  -50],
								[ 30, -17],
									])

		self.thruster_pts = np.array([
								[-5, -5],
								[ 5, -5],
								[ 5,  30],
								[-5,  30]
									])

		self.fire_pts = np.array([
								[-5, 30],
								[ 5, 30],
								[ 0, 30]
								])


		self.lander_pts = np.array([
								[-15,  17],
								[ 15,  17],
								[ 30,  42],
								[-15,  17],
								[-30,  42],
								[ 15,  17]
									])
	
	def draw_thrusters(self, rocket):
		left_thruster_angle = rocket.thruster_left_force_world_frame.get_angle() + np.pi/2
		left_thruster_pts = get_transformed_pts(self.thruster_pts, 
							left_thruster_angle, 
							rocket.left_thruster_pos, position_vector = False)
		cv2.polylines(self.canvas, [left_thruster_pts], True, rocket.thruster_color, 2)

		right_thruster_angle = rocket.thruster_right_force_world_frame.get_angle() + np.pi/2
		right_thruster_pts = get_transformed_pts(self.thruster_pts, 
							right_thruster_angle, 
							rocket.right_thruster_pos, position_vector = False)
		cv2.polylines(self.canvas, [right_thruster_pts], True, rocket.thruster_color, 2)

		right_thruster_fire_pts = self.fire_pts.copy()
		right_thruster_fire_pts[2, 1] += rocket.thruster_right_force_world_frame.get_magnitude()*3
		right_thruster_fire_pts = get_transformed_pts(right_thruster_fire_pts, 
							right_thruster_angle, 
							rocket.right_thruster_pos, position_vector = False)
		cv2.polylines(self.canvas, [right_thruster_fire_pts], True, rocket.fire_color, 2)


		left_thruster_fire_pts = self.fire_pts.copy()
		left_thruster_fire_pts[2, 1] += rocket.thruster_left_force_world_frame.get_magnitude()*3
		left_thruster_fire_pts = get_transformed_pts(left_thruster_fire_pts, 
							left_thruster_angle, 
							rocket.left_thruster_pos, position_vector = False)
		cv2.polylines(self.canvas, [left_thruster_fire_pts], True, rocket.fire_color, 2)


	def draw(self, rocket):
		body_pts = get_transformed_pts(self.rocket_body, rocket.orientation, rocket.pos)
		cv2.polylines(self.canvas, [body_pts], True, rocket.color, 2)
		
		top_pts = get_transformed_pts(self.rocket_top, rocket.orientation, rocket.pos)
		cv2.polylines(self.canvas, [top_pts], True, rocket.top_color, 2)

		lander_pts = get_transformed_pts(self.lander_pts, rocket.orientation, rocket.pos)
		cv2.polylines(self.canvas, [lander_pts], False, rocket.lander_color, 2)

		# cv2.polylines(self.canvas, [rocket.tail.astype("int")], False, rocket.lander_color, 1)
		self.draw_thrusters(rocket)



	def render(self):
		cv2.imshow("canvas", self.canvas)
		return cv2.waitKey(30)

	def clear(self):
		self.canvas = np.zeros((cfg.CANVAS_H, cfg.CANVAS_W, 3)).astype("uint8")