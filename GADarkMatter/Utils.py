import math
import random
import Evaluator
import matplotlib.pyplot as plt
import sys
data = {}


def flip(prob):
    return random.uniform(0, 1) < prob


def randInt(low, high):
    return random.randint(low, high - 1)


def decode(chrom, start, end):
    sum = 0
    for i in range(start, end):
        sum += chrom[i] * math.pow(2, end-i-1)
    return sum


def readfile(filename):
    global data
    data = {}
    data['radius'] = []
    data['e_obs'] = []
    data['v_obs'] = []
    data['v_gas'] = []
    data['v_disk'] = []
    data['v_bul'] = []
    data['inc'] = 0
    data['e_inc'] = 0
    data['Upsilon_D'] = 0
    data['Upsilon_B'] = 0
    data['e_Upsilon'] = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            vals = line.split()
            if len(vals) > 11:
                data['Upsilon_D'] = float(vals[1])
                data['Upsilon_B'] = float(vals[3])
                data['e_Upsilon'] = float(vals[2])
                data['inc'] = float(vals[7])
                data['e_inc'] = float(vals[8])
            else:
                data['radius'].append(float(vals[2]))
                data['v_obs'].append(float(vals[3]))
                data['e_obs'].append(float(vals[4]))
                data['v_gas'].append(float(vals[5]))
                data['v_disk'].append(float(vals[6]))
                data['v_bul'].append(float(vals[7]))


def uncorrelate_data():
    for i in range(len(data['v_obs'])):
        data['v_obs'][i] /= math.sin(math.radians(data['inc']))
        data['v_disk'][i] /= data['Upsilon_D']
        data['v_bul'][i] /= data['Upsilon_B']


def plot(U_b, U_d, theta, v_dm, outfile):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    v_disk = data['v_disk'].copy()
    v_bul = data['v_bul'].copy()
    v_obs = data['v_obs'].copy()
    v_exp = []
    for i in range(len(v_obs)):
        v_bul[i] *= U_b
        v_disk[i] *= U_d
        v_obs[i] *= math.sin(math.radians(theta))
        v_exp.append(math.sqrt(v_bul[i]**2 + v_disk[i]**2 + v_dm[i]**2 + data['v_gas'][i]**2))

    ax.plot(data['radius'], data['v_gas'], label='Gas', linestyle=':')
    ax.plot(data['radius'], v_bul, label='Bulge', linestyle='-.')
    ax.plot(data['radius'], v_disk, label='Disk', linestyle='--')
    ax.plot(data['radius'], v_dm, label='Dark Matter', linestyle='-')
    ax.plot(data['radius'], v_exp, label='Experimental RC', linestyle='-')
    ax.errorbar(data['radius'], v_obs, yerr=data['e_obs'], ecolor='black', label='Observed')
    ax.set_ylabel('V [km/s]')
    ax.set_xlabel('Radius [kpc]')
    plt.legend(prop={'size':7})
    fig.savefig(outfile)
    plt.close(fig)


def sortByObj(array):
    already_sorted = True
    for i in range(len(array)):
        for j in range(len(array) - i - 1):
            if array[j].objective > array[j + 1].objective:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array


def getDMVels(decvals, radii):
    arr = []
    for i in range(len(radii)):
        vdm = Evaluator.DM(decvals, radii[i])
        arr.append(vdm)
    return arr


def hammingDist(chr1, chr2):
    dist = 0
    for i in range(len(chr1)):
        if chr1[i] != chr2[1]:
            dist += 1
    return dist


def eucDist(decvals1, decvals2):
    dist = 0
    for i in range(len(decvals1)):
        dist += math.fabs((decvals1[i] - decvals2[i]) / decvals1[i])
    return dist
