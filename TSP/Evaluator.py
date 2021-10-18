
import Individual
import math
import random

def EucDist(point1, point2):
    x_diff = (float(point1[0]) - float(point2[0])) ** 2
    y_diff = (float(point1[1]) - float(point2[1])) ** 2
    return math.sqrt(x_diff + y_diff)

def EvalTSPEucDist(individual, options):
    sum = 0
    for i in range(individual.chromosomeLength - 1):
        sum += EucDist(options.cities[individual.chromosome[i]],
                       options.cities[individual.chromosome[i + 1]])
    return sum


def EvaluateOneMax(individual):
    sum = 0
    for i in range(len(individual.chromosome)):
        sum += individual.chromosome[i]

    return sum


