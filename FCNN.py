from controller import Controller
import numpy as np


class FCNN(Controller):
	def __init__(self, num_inputs, num_outputs, layers = []):
		Controller.__init__(self)
		self.name = "FCNN"
		self.num_inputs = num_inputs
		self.num_outputs = num_outputs
		self.layers = layers

		self.wts = np.random.random((self.num_outputs, self.num_inputs))*2 - 1
		# self.wts = np.ones((self.num_outputs, self.num_inputs)).astype("float16")

	def set_wts(self, wts):
		self.wts = wts.copy()

	def get_wts(self):
		return self.wts

	def __call__(self, inputs):
		outputs = self.wts@inputs
		outputs = np.tanh(outputs)
		# print(outputs.T)

		return self.get_force_vectors(outputs)