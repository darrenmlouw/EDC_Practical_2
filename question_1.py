import math
import numpy as np
import matplotlib.pyplot as plt
import statistics


class PRNG:
    def __init__(self):
        self.x = 1
        self.y = 1000
        self.z = 300
        self.temp = 0
        self.random = 0

    def randomUniform(self):
        # X Component
        self.x = 171 * (self.x % 177) - 2 * (self.x / 177)
        if self.x < 0:
            self.x = self.x + 30269
        # Y Component
        self.y = 172 * (self.y % 176) - 35 * (self.y / 176)
        if self.y < 0:
            self.y = self.y + 30307
        # Z Component
        self.z = 170 * (self.z % 178) - 63 * (self.z / 178)
        if self.z < 0:
            self.z = self.z + 30323
        # Addition of X, Y and Z Variable
        self.temp = self.x / 30269 + self.y / 30307 + self.z / 30323
        self.random = self.temp - math.trunc(self.temp)

        return self.random

# CODE FOR THE PDF GRAPH (Leave out if not in use)
# UNCOMMENT UNTIL ----
# print("Start")
# rand = PRNG()
# Array = []
# Max = 6000000
# total = 0
#
# for i in range(0, Max):
#     Array.append(rand.randomUniform())
#
# plt.hist(Array, bins=125, density=True)
# plt.figtext(0.83, 0.77, "\u03BC: "+str(round(statistics.mean(Array), 6)), ha='right')
# plt.figtext(0.83, 0.73, "\u03C3: " + str(round(statistics.stdev(Array), 6)), ha='right')
# plt.figtext(0.83, 0.69, "\u03C3 \u00b2: " + str(round(statistics.variance(Array), 6)), ha='right')
# plt.xlabel("x")
# plt.ylabel("Probability Density")
#
# plt.show()
# ----
