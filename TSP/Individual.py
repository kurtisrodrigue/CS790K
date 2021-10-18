import random
import Utils

class Individual:

	def __init__(self, options):
		self.chromosome = []
		self.chromosomeLength = options.chromosomeLength
		self.fitness = -1
		self.objective = -1
		self.rank = -1
		for i in range(options.chromosomeLength):
			self.chromosome.append(i)
		random.shuffle(self.chromosome)
		print(self.chromosome)

	def mutate(self, options):
		for i in range(options.chromosomeLength):
			if Utils.flip(options.pMut):
				out = random.randint(0, options.chromosomeLength-1)
				for j in range(options.chromosomeLength):
					if self.chromosome[j] == out:
						self.chromosome[j] = self.chromosome[i]
				self.chromosome[i] = out

