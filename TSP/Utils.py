
import random
import numpy as np

def flip(prob):
	return random.random() < prob

def randInt(low, high):
	return random.randint(low, high-1)

def swap(ind1, ind2):
	temp = ind1
	ind1 = ind2
	ind2 = temp
	return ind1, ind2

def valid_tour(chromosome):
	array = np.zeros(len(chromosome))
	for i in range(array.shape[0]):
		array[chromosome[i]] += 1
	for i in range(array.shape[0]):
		if array[i] > 1:
			return False
	return True


