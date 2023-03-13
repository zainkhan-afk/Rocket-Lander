from controller import Controller
import numpy as np
from copy import deepcopy


class FCNN(Controller):
	def __init__(self, num_inputs, num_outputs, layers = [20]):
		Controller.__init__(self)
		self.name = "FCNN"
		self.num_inputs = num_inputs
		self.num_outputs = num_outputs
		self.layers = layers

		self.layers = [self.num_inputs] + self.layers + [self.num_outputs]

		self.wts = []
		
		for i in range(len(self.layers)-1):
			in_neurons = self.layers[i]
			out_neurons = self.layers[i+1]

			layer_wts = np.random.random((in_neurons, out_neurons))*2 - 1
			self.wts.append(layer_wts)
		# self.wts = np.random.random((self.num_outputs, self.num_inputs))*2 - 1
		# self.wts = np.ones((self.num_outputs, self.num_inputs)).astype("float16")

	def set_wts(self, wts):
		self.wts = deepcopy(wts)

	def get_wts(self):
		return self.wts

	def __call__(self, inputs):
		outputs = inputs.copy()

		for i, layer_wts in enumerate(self.wts):
			outputs = layer_wts.T@outputs
			outputs = np.tanh(outputs)

		return self.get_force_vectors(outputs)