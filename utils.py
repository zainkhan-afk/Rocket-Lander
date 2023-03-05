import numpy as np
from vector import Vector

def get_transformed_pts(pts, angle, pos, position_vector = True):

	if position_vector:
		R = np.array([
						[np.cos(angle), -np.sin(angle), pos.x],
						[np.sin(angle),  np.cos(angle), pos.y]
					])
	else:
		R = np.array([
						[np.cos(angle), -np.sin(angle), pos[0, 0]],
						[np.sin(angle),  np.cos(angle), pos[0, 1]]
					])

	pts = np.append(pts, np.ones((pts.shape[0], 1)), axis = 1)
	new_pts = (R@pts.T).astype("int")
	return new_pts.T


def get_transformed_vector(in_vec, angle):
	R = np.array([
						[np.cos(angle), -np.sin(angle)],
						[np.sin(angle),  np.cos(angle)]
					])
	p = R@in_vec.as_numpy().T

	out_vec = Vector(x = p[0,0], y = p[1,0])
	return out_vec