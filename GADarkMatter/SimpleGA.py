
import random
import Options
import Utils
import time
import Evaluator
import Individual
import sys
from Population import Population
import matplotlib.pyplot as plt
seeds = [101101, 65, 92, 101, 821, 129, 2000, 2021, 2020, 430, 310, 209, 461, 102, 483, 1029, 2938, 47319, 21893, 2013,
         213, 4321, 4319, 2921, 4891, 4673, 2102, 4902, 1209, 9083]


class GA:

    def __init__(self):
        self.options = Options.Options()
        random.seed(self.options.randomSeed)


    def Init(self):
        self.parent = Population(self.options)
        self.parent.evaluate()
        self.parent.statistics()
        self.parent.report(0)
        self.child = Population(self.options)
        return

    def Run(self):
        fitnesses = []
        objs = []
        min = self.parent.min
        max = self.parent.max
        avg = self.parent.avg
        fitnesses.append([min, max, avg])
        min = self.parent.minObj
        max = self.parent.maxObj
        avg = self.parent.avgObj
        objs.append([min, max, avg])
        for	i in range(1, self.options.maxGen):
            start = time.time()
            self.parent.generation(self.child)
            self.child.evaluate()
            self.child.statistics()
            self.child.report(i)

            min = self.child.min
            max = self.child.max
            avg = self.child.avg
            fitnesses.append([min, max, avg])
            min = self.child.minObj
            max = self.child.maxObj
            avg = self.child.avgObj
            objs.append([min, max, avg])

            tmp = self.parent
            self.parent = self.child
            self.child = tmp
            if i % 10 == 0:
                chromosome = self.parent.getTopInd()
                decvals = Evaluator.decode_chromosome(chromosome, Utils.data)
                print(decvals)
                vdm = Utils.getDMVels(decvals, Utils.data['radius'])
                Utils.plot(decvals[5], decvals[6], decvals[7], vdm, 'Results/BestGen_{}.png'.format(i))
                print('best gen: {} decvals: {}'.format(i, decvals))
                chromosome = self.parent.getMidInd()
                decvals = Evaluator.decode_chromosome(chromosome, Utils.data)
                print(decvals)
                vdm = Utils.getDMVels(decvals, Utils.data['radius'])
                Utils.plot(decvals[5], decvals[6], decvals[7], vdm, 'Results/MidGen_{}.png'.format(i))
            end = time.time()
            print("Generation {} took {} seconds ".format(i, end-start))

        self.parent.printPop()
        return fitnesses, objs


if __name__ == "__main__":
    num_seeds = 30
    Utils.readfile('Data/UGC09133MassModel.mrt')
    Utils.uncorrelate_data()
    print('checkpoint:{}'.format(Utils.data))
    ga = GA()
    maxFits = []
    minFits = []
    avgFits = []
    maxObj = []
    minObj = []
    avgObj = []
    epochs = []
    for seed_index in range(num_seeds):
        # run GA with set seed found at the top of the file
        ga.options.randomSeed = seeds[seed_index]
        ga.Init()
        fitness, obj = ga.Run()

        # sum fitness and objectives to be averaged later
        if seed_index == 0:
            for i, item in enumerate(fitness):
                minFits.append(item[0])
                maxFits.append(item[1])
                avgFits.append(item[2])
                epochs.append(i)
        else:
            for i, item in enumerate(fitness):
                minFits[i] += item[0]
                maxFits[i] += item[1]
                avgFits[i] += item[2]
        if seed_index == 0:
            for i, item in enumerate(obj):
                minObj.append(item[0])
                maxObj.append(item[1])
                avgObj.append(item[2])
        else:
            for i, item in enumerate(obj):
                minObj[i] += item[0]
                maxObj[i] += item[1]
                avgObj[i] += item[2]

    # average out number of seeds
    for i in range(len(epochs)):
        minObj[i] /= num_seeds
        maxObj[i] /= num_seeds
        avgObj[i] /= num_seeds
        maxFits[i] /= num_seeds
        minFits[i] /= num_seeds
        avgFits[i] /= num_seeds

    # plot fitnesses
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((0, len(epochs)))
    ax.set_ylim((-1e6, 1e6))
    ax.plot(epochs, minFits, label="Min fitness", linestyle="-.")
    ax.plot(epochs, maxFits, label="Max fitness", linestyle="-")
    ax.plot(epochs, avgFits, label="Avg fitness", linestyle="--")
    ax.set_ylabel('Fitness value')
    ax.set_xlabel('Generation')
    fig.savefig('fitness_epochs.png')
    plt.close(fig)

    # plot objective function
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((0, len(epochs)))
    ax.set_ylim((0, 1e6))
    ax.plot(epochs, minObj, label="Min objective", linestyle="-.")
    ax.plot(epochs, maxObj, label="Max objective", linestyle="-")
    ax.plot(epochs, avgObj, label="Avg objective", linestyle="--")
    ax.set_ylabel('Objective value')
    ax.set_xlabel('Generation')
    fig.savefig('objective_epochs.png')
    plt.close(fig)

    with open('generation_info.txt', 'w') as f:
        f.write(str(minObj) + '\n')
        f.write(str(maxObj) + '\n')
        f.write(str(avgObj) + '\n')


