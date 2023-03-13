import numpy as np
from rocket import Rocket
from controller import Controller
from FCNN import FCNN
from simulator import Simulator
import random


class GeneticAlgorithm:
	def __init__(self, mutation_rate = 0.01, population = 10):
		self.original_mutation_rate = mutation_rate
		self.current_mutation_rate = mutation_rate
		self.population = population
		self.sim = Simulator(headless = False)
		self.prev_fittest = 0
		self.same_fitness_counter = 0

		self.all_entities = []

		for p in range(self.population):
			r = Rocket()
			c = FCNN(num_inputs = 10, num_outputs = 4)
			r.connect_controller(c)
			self.all_entities.append(r)

	def calc_fitness(self, rocket):
		if rocket.crashed:
			m = 1 - 100/rocket.time_alive
		else:
			m = 10


		angle_error = rocket.angle_error/rocket.time_alive
		return m*(rocket.points_collected + 1/rocket.dist + 1/angle_error)
		return m*(rocket.time_alive + 1/rocket.dist )*rocket.points_collected + 1/angle_error
		return rocket.time_alive * 1/angle_error

	def get_population_fitness(self):
		all_fitness = []
		for entity in self.all_entities:
			all_fitness.append(self.calc_fitness(entity))

		return all_fitness

	def create_new_population(self, fittest_idx):
		new_pop = []
		wts = self.all_entities[fittest_idx].controller.get_wts()
		for p in range(self.population):
			r = Rocket()
			if p == 0:
				r.top_g = True
			c = FCNN(num_inputs = 10, num_outputs = 4)
			c.set_wts(wts)
			r.connect_controller(c)
			new_pop.append(r)

		return new_pop

	def mutate_wts(self, wts, mutation_rate):
		for layer_wts in wts:
			R, C = layer_wts.shape

			for r in range(R):
				for c in range(C):
					if np.random.random()<mutation_rate:
						layer_wts[r, c] = np.random.normal()

		return wts

	def mutate_population(self, pop):
		pop_50_percent = int(0.5*self.population)
		for p in range(1, self.population):
			wts = pop[p].controller.get_wts()
			if p<pop_50_percent:
				wts = self.mutate_wts(wts, self.original_mutation_rate)
			else:
				wts = self.mutate_wts(wts, self.current_mutation_rate)
			pop[p].controller.set_wts(wts)

		return pop


	def evaluate(self):
		num_survivors = len(self.all_entities)
		self.sim.t = 0
		self.all_entities.reverse()
		while num_survivors != 0:
			k = self.sim.step(self.all_entities)
			if self.sim.t >= 1000:
				break

			num_survivors = sum([1 if entity.is_alive() else 0 for entity in self.all_entities])

			if k == ord("q"):
				exit()

		all_fitness = self.get_population_fitness()
		highest_fitness = max(all_fitness)
		
		if highest_fitness == self.prev_fittest:
			self.same_fitness_counter += 1
		else:
			self.same_fitness_counter = 0
			self.current_mutation_rate = self.original_mutation_rate

		if self.same_fitness_counter>5:
			self.current_mutation_rate += 0.02
			if self.current_mutation_rate>0.5:
				self.current_mutation_rate = 0.5
			print(f"Increasing mutation rate to: {self.current_mutation_rate}")

		self.prev_fittest = highest_fitness

		
		fittest_idx = all_fitness.index(highest_fitness)
		print(f"Fittest: {highest_fitness}\n\n")

		self.all_entities = self.create_new_population(fittest_idx)
		self.all_entities = self.mutate_population(self.all_entities)



if __name__ == "__main__":
	GA = GeneticAlgorithm(population = 500)
	for g in range(1001):
		if g%10 == 0:
			GA.sim.headless = False
		else:
			GA.sim.headless = True
		print(f"Generation: {g}")
		GA.evaluate()