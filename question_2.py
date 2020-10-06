import math
import numpy as np
import matplotlib.pyplot as plt
import question_1
import statistics

rand = question_1.PRNG()


class GRNG:
    def __init__(self):
        self.probability = 0
        self.u1 = 0
        self.u2 = 0
        self.u3 = 0
        self.v1 = 0
        self.v2 = 0
        self.random = 0
        self.x = 0
        self.y = 0
        self.g3 = 0
        self.negative1 = 0
        self.negative2 = 0

    def getNewProb(self):
        self.u1 = rand.randomUniform()
        self.u2 = rand.randomUniform()
        self.u3 = rand.randomUniform()
        self.v1 = rand.randomUniform()
        self.v2 = rand.randomUniform()
        self.probability = rand.randomUniform()
        self.negative1 = rand.randomUniform()
        self.negative2 = rand.randomUniform()
        if self.negative1 > 0.5:
            self.v1 = -1 * self.v1

        if self.negative2 > 0.5:
            self.v2 = -1 * self.v2

    def S3(self):
        if abs(self.x) < 1:
            self.g3 = 17.49731196 * math.exp(-0.5 * self.x * self.x) - 4.73570326 * (
                    3 - self.x * self.x) - 2.15787544 * (1.5 - abs(self.x))

        elif 1 < abs(self.x) < 1.5:
            self.g3 = 17.49731196 * math.exp(-0.5 * self.x * self.x) - 2.36785163 * pow(3 - abs(self.x), 2) -\
                      2.15787544 * (1.5 - abs(self.x))

        elif 1.5 < abs(self.x) < 3:
            self.g3 = 17.49731196 * math.exp(-0.5 * self.x * self.x) - 2.36785163 * pow(3 - abs(self.x), 2)
        elif abs(self.x) > 3:
            self.g3 = 0

    def randomNormal(self):
        self.getNewProb()

        # Step 1
        if self.probability < 0.8638:
            self.random = 2 * (self.u1 + self.u2 + self.u3 - 1.5)
        # Step 2
        elif 0.9745 > self.probability >= 0.8638:
            self.random = 1.5 * (self.u1 + self.u2 - 1)
        # Step 3
        elif 0.9973002039 > self.probability >= 0.9745:
            self.y = 1
            self.g3 = 0
            while self.y > self.g3:
                self.getNewProb()
                self.x = 6 * self.u1 - 3
                self.y = 0.358 * self.u2
                self.S3()
            self.random = self.x
        # Step 4
        else:
            while abs(self.x) < 3 and abs(self.y) < 3:
                self.getNewProb()
                self.x = self.v1 * ((9 - 2 * math.log((self.v1 ** 2 + self.v2 ** 2), 10)) / (
                        self.v1 ** 2 + self.v2 ** 2)) ** 0.5
                self.y = self.v2 * ((9 - 2 * math.log((self.v1 ** 2 + self.v2 ** 2), 10)) / (
                        self.v1 ** 2 + self.v2 ** 2)) ** 0.5

            if abs(self.x) > 3:
                self.random = self.x
            elif abs(self.y) > 3:
                self.random = self.y

        return self.random

# CODE FOR THE PDF GRAPH (Leave out if not in use)
# UNCOMMENT UNTIL ----
# normal = GRNG()
# Array = []
# Max = 4000000 #use 4mil
# total = 0
# for i in range(0, Max):
#     Array.append(normal.randomNormal())
#
# plt.hist(Array, bins=125, density=True)
# plt.figtext(0.85, 0.8, "\u03BC: "+str(round(statistics.mean(Array), 6)), ha='right')
# plt.figtext(0.85, 0.76, "\u03C3: " + str(round(statistics.stdev(Array), 6)), ha='right')
# plt.figtext(0.85, 0.72, "\u03C3 \u00b2: " + str(round(statistics.variance(Array), 6)), ha='right')
# plt.xlabel("x")
# plt.ylabel("Probability Density")
#
# plt.show()
# ----
