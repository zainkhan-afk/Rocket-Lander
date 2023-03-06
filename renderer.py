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
								[-30, -15],
								[ 0,  -50],
								[ 30, -15],
									])

		self.thruster_pts = np.array([
								[-5,  -5],
								[ 0, -10],
								[ 5,  -5],
								[ 5,  30],
								[-5,  30]
									])

		self.fire_pts = np.array([
								[-5, 30],
								[ 0, 30],
								[ 5, 30],
								[ 0, 30]
								])


		self.lander_pts = np.array([
								[-15,  15],
								[ 15,  15],
								[ 30,  40],
								[-15,  15],
								[-30,  40],
								[ 15,  15]
									])
	

	def draw_flame_shade(self, rocket, left_thruster_angle, right_thruster_angle, flame_type = 1):
		if flame_type == 2:
			multiplier1 = 0.2
			multiplier2 = 2
			multiplier3 = 0.15
			flame_color = rocket.fire_color2
		elif flame_type == 3:
			multiplier1 = 0.2
			multiplier2 = 1.5
			multiplier3 = 0.1
			flame_color = rocket.fire_color3
		else:
			multiplier1 = 0.2
			multiplier2 = 3
			multiplier3 = 0.2
			flame_color = rocket.fire_color1

		right_thruster_fire_pts = self.fire_pts.copy()
		right_thruster_fire_pts[0, 1] += rocket.thruster_right_force_world_frame.get_magnitude()*multiplier1
		right_thruster_fire_pts[2, 1] += rocket.thruster_right_force_world_frame.get_magnitude()*multiplier1
		right_thruster_fire_pts[3, 1] += rocket.thruster_right_force_world_frame.get_magnitude()*multiplier2

		right_thruster_fire_pts[0, 0] += rocket.thruster_right_force_world_frame.get_magnitude()*multiplier3
		right_thruster_fire_pts[2, 0] -= rocket.thruster_right_force_world_frame.get_magnitude()*multiplier3

		right_thruster_fire_pts = get_transformed_pts(right_thruster_fire_pts, 
							right_thruster_angle, 
							rocket.right_thruster_pos, position_vector = False)
		# cv2.polylines(self.canvas, [right_thruster_fire_pts], True, flame_color, 2)
		cv2.fillPoly(self.canvas, [right_thruster_fire_pts], flame_color)


		left_thruster_fire_pts = self.fire_pts.copy()
		left_thruster_fire_pts[0, 1] += rocket.thruster_left_force_world_frame.get_magnitude()*multiplier1
		left_thruster_fire_pts[2, 1] += rocket.thruster_left_force_world_frame.get_magnitude()*multiplier1
		left_thruster_fire_pts[3, 1] += rocket.thruster_left_force_world_frame.get_magnitude()*multiplier2

		left_thruster_fire_pts[0, 0] += rocket.thruster_left_force_world_frame.get_magnitude()*multiplier3
		left_thruster_fire_pts[2, 0] -= rocket.thruster_left_force_world_frame.get_magnitude()*multiplier3
		left_thruster_fire_pts = get_transformed_pts(left_thruster_fire_pts, 
							left_thruster_angle, 
							rocket.left_thruster_pos, position_vector = False)
		# cv2.polylines(self.canvas, [left_thruster_fire_pts], True, rocket.fire_color, 2)
		cv2.fillPoly(self.canvas, [left_thruster_fire_pts], flame_color)

	def draw_flames(self, rocket, left_thruster_angle, right_thruster_angle):
		self.draw_flame_shade(rocket, left_thruster_angle, right_thruster_angle, flame_type = 1)
		self.draw_flame_shade(rocket, left_thruster_angle, right_thruster_angle, flame_type = 2)
		self.draw_flame_shade(rocket, left_thruster_angle, right_thruster_angle, flame_type = 3)
		# right_thruster_fire_pts = self.fire_pts.copy()
		# right_thruster_fire_pts[0, 1] += rocket.thruster_right_force_world_frame.get_magnitude()*0.1
		# right_thruster_fire_pts[2, 1] += rocket.thruster_right_force_world_frame.get_magnitude()*0.1
		# right_thruster_fire_pts[3, 1] += rocket.thruster_right_force_world_frame.get_magnitude()*3
		# right_thruster_fire_pts = get_transformed_pts(right_thruster_fire_pts, 
		# 					right_thruster_angle, 
		# 					rocket.right_thruster_pos, position_vector = False)
		# # cv2.polylines(self.canvas, [right_thruster_fire_pts], True, rocket.fire_color, 2)
		# cv2.fillPoly(self.canvas, [right_thruster_fire_pts], rocket.fire_color1)


		# left_thruster_fire_pts = self.fire_pts.copy()
		# left_thruster_fire_pts[0, 1] += rocket.thruster_left_force_world_frame.get_magnitude()*0.1
		# left_thruster_fire_pts[2, 1] += rocket.thruster_left_force_world_frame.get_magnitude()*0.1
		# left_thruster_fire_pts[3, 1] += rocket.thruster_left_force_world_frame.get_magnitude()*3
		# left_thruster_fire_pts = get_transformed_pts(left_thruster_fire_pts, 
		# 					left_thruster_angle, 
		# 					rocket.left_thruster_pos, position_vector = False)
		# # cv2.polylines(self.canvas, [left_thruster_fire_pts], True, rocket.fire_color, 2)
		# cv2.fillPoly(self.canvas, [left_thruster_fire_pts], rocket.fire_color1)
		# cv2.fillPoly(self.canvas, [(left_thruster_fire_pts*0.8).astype("int")], rocket.fire_color2)

	def draw_thrusters(self, rocket):
		left_thruster_angle = rocket.thruster_left_force_world_frame.get_angle() + np.pi/2
		left_thruster_pts = get_transformed_pts(self.thruster_pts, 
							left_thruster_angle, 
							rocket.left_thruster_pos, position_vector = False)
		# cv2.polylines(self.canvas, [left_thruster_pts], True, rocket.thruster_color, 2)
		cv2.fillPoly(self.canvas, [left_thruster_pts], rocket.thruster_color)

		right_thruster_angle = rocket.thruster_right_force_world_frame.get_angle() + np.pi/2
		right_thruster_pts = get_transformed_pts(self.thruster_pts, 
							right_thruster_angle, 
							rocket.right_thruster_pos, position_vector = False)
		# cv2.polylines(self.canvas, [right_thruster_pts], True, rocket.thruster_color, 2)
		cv2.fillPoly(self.canvas, [right_thruster_pts], rocket.thruster_color)

		self.draw_flames(rocket, left_thruster_angle, right_thruster_angle)


	def draw(self, rocket):
		body_pts = get_transformed_pts(self.rocket_body, rocket.orientation, rocket.pos)
		# cv2.polylines(self.canvas, [body_pts], True, rocket.color, 2)
		cv2.fillPoly(self.canvas, [body_pts], rocket.color)
		
		top_pts = get_transformed_pts(self.rocket_top, rocket.orientation, rocket.pos)
		# cv2.polylines(self.canvas, [top_pts], True, rocket.top_color, 2)
		cv2.fillPoly(self.canvas, [top_pts], rocket.top_color)

		lander_pts = get_transformed_pts(self.lander_pts, rocket.orientation, rocket.pos)
		cv2.polylines(self.canvas, [lander_pts], False, rocket.lander_color, 2)

		# cv2.polylines(self.canvas, [rocket.tail.astype("int")], False, rocket.lander_color, 1)
		self.draw_thrusters(rocket)



	def render(self):
		cv2.imshow("canvas", self.canvas)
		return cv2.waitKey(30)

	def clear(self):
		self.canvas = np.zeros((cfg.CANVAS_H, cfg.CANVAS_W, 3)).astype("uint8")