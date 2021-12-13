
import Individual
import math
import time
import random
from scipy.integrate import quad
import Utils


def func(x, p, a, b, g, s):
    return ((x**2) * p) / (((x / s) ** g) * (1 + (x / s) ** a) ** ((b - g) / a))


def decode(chrom, start, end):
    sum = 0
    for i in range(start, end):
        sum += chrom[i] * math.pow(2, end-i-1)
    return sum


def decode_chromosome(chromosome, data):
    mins = [1e3, 0.1, 2, 0.1, 0.5, data['Upsilon_B'] - data['e_Upsilon'], data['Upsilon_D'] - data['e_Upsilon'],
            data['inc'] - data['e_inc']]
    maxs = [5e8, 3, 3.5, 2, 110, data['Upsilon_B'] + data['e_Upsilon'], data['Upsilon_D'] + data['e_Upsilon'],
            data['inc'] + data['e_inc']]
    var_sizes = [10, 10, 10, 10, 10, 10, 10, 10]
    clength = len(mins)
    decvals = []
    j = 0
    for i in range(clength):
        precision = (maxs[i] - mins[i]) / math.pow(2, var_sizes[i])
        x = chromosome[j:j + var_sizes[i] - 1]
        val = decode(x, 0, len(x))
        decval = mins[i] + precision * val
        j += var_sizes[i]
        decvals.append(decval)
    return decvals


def DM(decvals, radius):
    G = 4.3e-6
    vdm = G / radius
    integral = quad(func, 0, radius, args=(decvals[0], decvals[1], decvals[2], decvals[3], decvals[4]),
                    limit=200)
    vdm *= 4 * math.pi * integral[0]
    return vdm


def EvaluateDM(chromosome, data):
    decvals = decode_chromosome(chromosome, data)
    error = 0

    for k in range(len(data['radius'])):
        vdm = DM(decvals, data['radius'][k])
        v2 = vdm**2 + (decvals[5] * data['v_bul'][k])**2 + (decvals[6] * data['v_disk'][k])**2 + data['v_gas'][k]**2
        error += math.fabs(v2 - ((math.sin(math.radians(decvals[7]))*data['v_obs'][k])**2))**2 / ((math.sin(math.radians(decvals[7])) * data['v_obs'][k]) ** 2)
    return error


def EvaluateDMDecVals(decvals, data):
    error = 0
    for k in range(len(data['radius'])):
        vdm = DM(decvals, data['radius'][k])
        v2 = vdm ** 2 + (decvals[5] * data['v_bul'][k]) ** 2 + (decvals[6] * data['v_disk'][k]) ** 2 + data['v_gas'][k] ** 2
        error += math.fabs(v2 - ((math.sin(math.radians(decvals[7])) * data['v_obs'][k]) ** 2))**2 / ((math.sin(math.radians(decvals[7])) * data['v_obs'][k]) ** 2)
    return error


