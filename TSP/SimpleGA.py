
import random
import Options
from Population import Population
import matplotlib.pyplot as plt
seeds = [10, 65, 92, 101, 821, 129, 2000, 2021, 2020, 430, 310, 209, 461, 102, 483, 1029, 2938, 47319, 21893, 2013,
         213, 4321, 4319, 2921, 4891, 4673, 2102, 4902, 1209, 9083]
filename = 'Problems/berlin52.tsp'

class GA:

    def __init__(self):
        self.options = Options.Options()
        random.seed(self.options.randomSeed)
        with open(filename) as f:
            lines = f.readlines()
            for i in range(6, len(lines)):
                if lines[i] != 'EOF\n':
                    numbers = lines[i].split()
                    print(numbers)
                    self.options.cities.append([numbers[1], numbers[2]])
                else:
                    break
        self.options.chromosomeLength = len(self.options.cities)



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
        for	i in range(1, self.options.maxGen):
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

        self.parent.printPop()
        return fitnesses, objs


if __name__ == "__main__":
    num_seeds = 1
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
        print('running simulation #{}'.format(seed_index))

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

    print('number of evals: {}'.format(ga.parent.evals + ga.child.evals))

    # plot fitnesses
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(epochs, minFits, label="Min fitness", linestyle="-.")
    ax.plot(epochs, maxFits, label="Max fitness", linestyle="-")
    ax.plot(epochs, avgFits, label="Avg fitness", linestyle="--")
    plt.show()

    # pliot objective function
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(epochs, minObj, label="Min objective", linestyle="-.")
    ax.plot(epochs, maxObj, label="Max objective", linestyle="-")
    ax.plot(epochs, avgObj, label="Avg objective", linestyle="--")
    plt.show()


