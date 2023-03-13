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
								[ 0,  -40],
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
								[-20,  15],
								[ 20,  15],
								[ 40,  40],
								[-20,  15],
								[-40,  40],
								[ 20,  15]
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
		# cv2.polylines(self.canvas, [right_thruster_fire_pts], True, flame_color, 1)
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
		# cv2.polylines(self.canvas, [left_thruster_fire_pts], True, flame_color, 1)
		cv2.fillPoly(self.canvas, [left_thruster_fire_pts], flame_color)

	def draw_flames(self, rocket, left_thruster_angle, right_thruster_angle):
		self.draw_flame_shade(rocket, left_thruster_angle, right_thruster_angle, flame_type = 1)
		self.draw_flame_shade(rocket, left_thruster_angle, right_thruster_angle, flame_type = 2)
		self.draw_flame_shade(rocket, left_thruster_angle, right_thruster_angle, flame_type = 3)

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

		pt1 = (int(rocket.pos.x - cfg.ROCKET_W//2), int(rocket.pos.y - cfg.ROCKET_H//2))
		pt2 = (int(rocket.pos.x + cfg.ROCKET_W//2), int(rocket.pos.y + cfg.ROCKET_H//2))
		cv2.rectangle(self.canvas, pt1, pt2, (0, 255, 0), 1)


	def draw(self, rocket):
		body_pts = get_transformed_pts(self.rocket_body, rocket.orientation, rocket.pos)
		# cv2.polylines(self.canvas, [body_pts], True, rocket.color, 2)
		if rocket.top_g:
			cv2.fillPoly(self.canvas, [body_pts], rocket.color_w)
		else:
			cv2.fillPoly(self.canvas, [body_pts], rocket.color)
		
		top_pts = get_transformed_pts(self.rocket_top, rocket.orientation, rocket.pos)
		# cv2.polylines(self.canvas, [top_pts], True, rocket.top_color, 2)
		cv2.fillPoly(self.canvas, [top_pts], rocket.top_color)

		lander_pts = get_transformed_pts(self.lander_pts, rocket.orientation, rocket.pos)
		cv2.polylines(self.canvas, [lander_pts], False, rocket.lander_color, 2)

		# cv2.polylines(self.canvas, [rocket.tail.astype("int")], False, rocket.lander_color, 1)
		self.draw_thrusters(rocket)
		pt = (int(rocket.pos.x), int(rocket.pos.y))
		cv2.circle(self.canvas, (rocket.goal[0], rocket.goal[1]), 5,  (0, 255, 0), -1)



	def render(self):
		cv2.imshow("canvas", self.canvas)
		return cv2.waitKey(1)

	def clear(self):
		self.canvas = np.zeros((cfg.CANVAS_H, cfg.CANVAS_W, 3)).astype("uint8")