import copy
import Individual
import Evaluator
import random
import Utils

class Population(object):

	def	__init__(self, options):
		self.options = options
		self.individuals = []
		self.min = -1
		self.max = -1
		self.avg = -1
		self.minObj = -1
		self.maxObj = 100000
		self.avgObj = -1
		self.evals = 0
		# initialize population with randomly generated Individuals
		for i in range(options.populationSize):
			self.individuals.append(Individual.Individual(options))
		self.evaluate()

	def evaluate(self):
		for ind in self.individuals:
			ind.objective = Evaluator.EvalTSPEucDist(ind, self.options)
			self.evals += 1
		self.generateFitness()

	def generateFitness(self):
		for ind in self.individuals:
			ind.fitness = 0 - ind.objective

	def printPop(self):
			i = 0
			for ind in self.individuals:
				print(i, end=": ")
				print (ind.chromosome, " Fit: ", ind.fitness)
				i = i+1
			self.report("")

	def report(self, gen):
		print (gen, self.min, self.avg, self.max)

	def sortByFitness(self, array):
		already_sorted = True
		# simply bubble sort. will change if it takes too long
		for i in range(len(array)):
			for j in range(len(array) - i - 1):
				if array[j].fitness > array[j + 1].fitness:
					array[j], array[j + 1] = array[j + 1], array[j]
					already_sorted = False
			if already_sorted:
				break


	def rankIndividuals(self):
		self.sortByFitness(self.individuals)
		for i in range(len(self.individuals)):
			self.individuals[i].rank = i + 1
			self.sumRank += i + 1

	def statistics(self):
		self.sumFitness = 0
		self.sumRank = 0
		self.sumObj = 0
		self.min = self.individuals[0].fitness
		self.minObj = self.individuals[0].objective
		self.max = self.individuals[0].fitness
		self.maxObj = self.individuals[0].objective
		self.avg = 0
		for ind in self.individuals:
			self.sumFitness += ind.fitness
			self.sumObj += ind.objective
			if ind.fitness < self.min:
				self.min = ind.fitness
			if ind.fitness > self.max:
				self.max = ind.fitness
			if ind.objective < self.minObj:
				self.minObj = ind.objective
			if ind.objective > self.maxObj:
				self.maxObj = ind.objective
			if not Utils.valid_tour(ind.chromosome):
				print('INVALID CHROMOSOME: {}').format(ind.chromosome)
				exit()


		self.avg = self.sumFitness/len(self.individuals)
		self.avgObj = self.sumObj /len(self.individuals)
		self.rankIndividuals()

	def select(self):
		randFraction = self.sumRank * random.uniform(0, 1)
		sum = 0
		i = 0
		for ind in self.individuals:
			sum += ind.rank
			if randFraction <= sum:
				return (i, ind)
			i = i + 1
		print("Selection failed")
		return (len(self.individuals) - 1, self.individuals[-1])

	def generation(self, child):
		for i in range(0, len(self.individuals), 2):
			x, p1 = self.select()
			x, p2 = self.select()
			while p1 == p2:
				x, p2 = self.select()
			c1 = child.individuals[i]
			c2 = child.individuals[i + 1]

			self.PMX(p1, p2, c1, c2)
			c1.mutate(self.options)
			c2.mutate(self.options)
		# CHC selection
		self.generateFitness()
		self.statistics()
		temp = self.individuals.copy()
		temp.extend(child.individuals.copy())
		self.sortByFitness(temp)
		for i in range(len(self.individuals)):
			self.individuals[i] = copy.deepcopy(temp[i])
		self.generateFitness()
		self.statistics()



	def PMX(self, p1, p2, c1, c2):
		for i in range(self.options.chromosomeLength):
			c1.chromosome[i] = p1.chromosome[i]
			c2.chromosome[i] = p2.chromosome[i]
		if Utils.flip(self.options.pCross):
			flipped_bits = []
			point1 = random.randint(0, self.options.chromosomeLength-1)
			point2 = random.randint(0, self.options.chromosomeLength-1)
			if point2 < point1:
				point2, point1 = point1, point2
			for i in range(point1, point2+1):
				c1.chromosome[i] = p2.chromosome[i]
				c2.chromosome[i] = p1.chromosome[i]
				flipped_bits.append([p1.chromosome[i], p2.chromosome[i]])
			while not Utils.valid_tour(c1.chromosome) or not Utils.valid_tour(c2.chromosome):
				for i in range(point1):
					for j in range(len(flipped_bits)):
						if c1.chromosome[i] == flipped_bits[j][1]:
							c1.chromosome[i] = flipped_bits[j][0]
						if c2.chromosome[i] == flipped_bits[j][0]:
							c2.chromosome[i] = flipped_bits[j][1]
				for i in range(point2+1, self.options.chromosomeLength):
					for j in range(len(flipped_bits)):
						if c1.chromosome[i] == flipped_bits[j][1]:
							c1.chromosome[i] = flipped_bits[j][0]
						if c2.chromosome[i] == flipped_bits[j][0]:
							c2.chromosome[i] = flipped_bits[j][1]





'''
		for i in range(self.options.chromosomeLength):
			c1.chromosome[i] = p1.chromosome[i]
			c2.chromosome[i] = p2.chromosome[i]
		if Utils.flip(self.options.pCross):
			xp = Utils.randInt(1, self.options.chromosomeLength)
			for i in range(xp, self.options.chromosomeLength):
				c1.chromosome[i] = p2.chromosome[i]
				c2.chromosome[i] = p1.chromosome[i]
'''