import Individual
import Evaluator
import random
import Utils
import time
import copy
from joblib import Parallel, delayed


class Population(object):

    def __init__(self, options):
        self.options = options
        self.individuals = []
        self.min = -1
        self.max = -1
        self.avg = -1
        self.minObj = -1
        self.maxObj = -1
        self.avgObj = -1
        self.evals = 0
        self.sumRank = 1
        # initialize population with randomly generated Individuals
        for i in range(options.populationSize):
            self.individuals.append(Individual.Individual(options))
        self.evaluate()

    def getTopInd(self):
        print(self.individuals[0].objective)
        return self.individuals[0].chromosome

    def getMidInd(self):
        return self.individuals[int(len(self.individuals)/2)].chromosome

    def evaluate(self):
        results = Parallel(n_jobs=-1) \
            (delayed(Evaluator.EvaluateDM)(chromosome=ind.chromosome, data=Utils.data) \
             for ind in self.individuals)
        for i in range(len(results)):
            self.individuals[i].objective = results[i]
        self.generateFitness()
        self.rankIndividuals()

    def printPop(self):
        i = 0
        for ind in self.individuals:
            print(i, end=": ")
            print(ind.chromosome, " Fit: ", ind.fitness)
            i = i + 1
        self.report("")

    def rankIndividuals(self):
        Utils.sortByObj(self.individuals)
        self.sumRank = 0
        for i in range(len(self.individuals)):
            self.individuals[i].rank = len(self.individuals) - i
            self.sumRank += len(self.individuals) - i


    def generateFitness(self):
        for ind in self.individuals:
            ind.fitness = 1000000 - ind.objective

    def report(self, gen):
        print(gen, self.min, self.avg, self.max)

    def statistics(self):
        self.sumFitness = 0
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

        self.avg = self.sumFitness / len(self.individuals)
        self.avgObj = self.sumObj / len(self.individuals)
        self.rankIndividuals()

    def select(self):
        randFraction = self.sumRank * random.uniform(0, 1)
        tempsum = 0
        i = 0
        for ind in self.individuals:
            tempsum += ind.rank
            if randFraction <= tempsum:
                return i, ind
            i = i + 1
        print("Selection failed: {} out of {}, rank: {}".format(tempsum, randFraction, self.sumRank))

        rand = Utils.randInt(0, len(self.individuals))
        return rand, self.individuals[rand]

    def xovermut(self, child, i, data):
        x, p1 = self.select()
        y, p2 = self.select()

        c1 = child.individuals[i]
        c2 = child.individuals[i + 1]

        self.xoverUniform(p1, p2, c1, c2)
        c1.mutate(self.options, data)
        c2.mutate(self.options, data)
        c1.objective = Evaluator.EvaluateDM(c1.chromosome, data)
        c2.objective = Evaluator.EvaluateDM(c2.chromosome, data)
        return [c1, c2]

    def xovermutGeno(self, child, i, data):
        x, p1 = self.select()
        y, p2 = self.select()

        c1 = child.individuals[i]
        c2 = child.individuals[i + 1]

        dist = Utils.hammingDist(p1.chromosome, p2.chromosome)
        while 20 < dist and x != y:
            x, p1 = self.select()
            y, p2 = self.select()
            dist = Utils.hammingDist(p1.chromosome, p2.chromosome)

        self.xoverUniform(p1, p2, c1, c2)
        c1.mutate(self.options, data)
        c2.mutate(self.options, data)
        c1.objective = Evaluator.EvaluateDM(c1.chromosome, data)
        c2.objective = Evaluator.EvaluateDM(c2.chromosome, data)
        return [c1, c2]

    def xovermutPheno(self, child, i, data):
        x, p1 = self.select()
        y, p2 = self.select()

        c1 = child.individuals[i]
        c2 = child.individuals[i + 1]

        p1vals = Evaluator.decode_chromosome(p1.chromosome, data)
        p2vals = Evaluator.decode_chromosome(p2.chromosome, data)
        dist = Utils.eucDist(p1vals, p2vals)
        while 1 < dist and x != y:
            x, p1 = self.select()
            y, p2 = self.select()
            p1vals = Evaluator.decode_chromosome(p1.chromosome, data)
            p2vals = Evaluator.decode_chromosome(p2.chromosome, data)
            dist = Utils.eucDist(p1vals, p2vals)

        self.xoverUniform(p1, p2, c1, c2)
        c1.mutate(self.options, data)
        c2.mutate(self.options, data)
        c1.objective = Evaluator.EvaluateDM(c1.chromosome, data)
        c2.objective = Evaluator.EvaluateDM(c2.chromosome, data)
        return [c1, c2]

    def generation(self, child):
        # X-over and mutation
        results = Parallel(n_jobs=-1) \
            (delayed(self.xovermutGeno)(child=child, i=i, data=Utils.data) \
                for i in range(0, len(self.individuals), 2))

        for i in range(0, len(self.individuals), 2):
            j = int(i/2)
            Utils.sortByObj(results[j])
            child.individuals[i].copyInd(results[j][0])
            child.individuals[i+1].copyInd(results[j][1])

        temp = child.individuals.copy()
        temp.extend(self.individuals.copy())
        Utils.sortByObj(temp)
        for i in range(len(self.individuals)):
            child.individuals[i].copyInd(temp[i])



    def xoverUniform(self, p1, p2, c1, c2):
        for i in range(self.options.chromosomeLength):
            c1.chromosome[i] = p1.chromosome[i]
            c2.chromosome[i] = p2.chromosome[i]
        for i in range(self.options.chromosomeLength):
            if Utils.flip(self.options.pCross):
                c2.chromosome[i] = p1.chromosome[i]
                c1.chromosome[i] = p2.chromosome[i]
