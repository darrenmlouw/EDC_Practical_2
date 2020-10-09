import question_1
import question_2
import math
import matplotlib.pyplot as plt
import random

from termcolor import colored

uniformNumber = question_1.PRNG()
noiseNumber = question_2.GRNG()


# Comment

class MLSE:
    def __init__(self, bits, numM):
        self.N = 200
        self.rt = []  # [[0 for x in range(200)] for y in range(15)]
        self.s = []
        self.delta = []
        self.alpha = []
        self.cStatic = [complex(0.89, 0.92), complex(0.42, 0.37), complex(0.19, 0.12)]
        self.cDynamic = [complex(0, 0), complex(0, 0), complex(0, 0)]
        self.total = bits
        self.bits = []
        self.symbols = []
        self.rk = []
        self.transmittedSymbols = []
        self.transmittedBits = []
        self.SNR = 0
        self.Eb = 0
        self.N0 = 0
        self.sigma = 0
        self.M = numM
        self.bitErrorCount = 0
        self.symErrorCount = 0
        self.BER = []
        self.SER = []

    def binary(self):
        temp = random.random()
        if temp > 0.5:
            self.bits.append(1)
        else:
            self.bits.append(0)

    def newDynamic(self):
        self.cDynamic = [complex(random.gauss(0, 1), random.gauss(0, 1)) / (math.sqrt(2 * 3)),
                         complex(random.gauss(0, 1), random.gauss(0, 1)) / (math.sqrt(2 * 3)),
                         complex(random.gauss(0, 1), random.gauss(0, 1)) / (math.sqrt(2 * 3))]


# ----------------------------------------------------------------
# Initialize
# ----------------------------------------------------------------
print("Start")
BPSK = MLSE(200000, 2)
QAM4 = MLSE(400000, 4)
PSK8 = MLSE(600000, 8)
print(1)
# ----------------------------------------------------------------
# Set Bits and Symbols
# ----------------------------------------------------------------
for i in range(0, BPSK.total):
    BPSK.binary()
    length = len(BPSK.bits)
    if BPSK.bits[length - 1] == 1:
        BPSK.symbols.append(1)
    else:
        BPSK.symbols.append(-1)
print(2)

# print("BPSK Bits: " + str(BPSK.bits))
# print("BPSK Symb: " + str(BPSK.symbols))
# print()

# Setting bits and symbols
duo = [0] * 2
for i in range(QAM4.total):
    QAM4.binary()
    duo[i % 2] = QAM4.bits[i]
    if (i % 2 + 1) == 2:
        if duo[0] == 0 and duo[1] == 0:
            QAM4.symbols.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))

        elif duo[0] == 0 and duo[1] == 1:
            QAM4.symbols.append(complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))

        elif duo[0] == 1 and duo[1] == 1:
            QAM4.symbols.append(complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))

        elif duo[0] == 1 and duo[1] == 0:
            QAM4.symbols.append(complex(1 / math.sqrt(2), -1 / math.sqrt(2)))

# print("4QAM Bits: " + str(QAM4.bits))
# print("4QAM Symb: " + str(QAM4.symbols))
# print()
print(3)

# Setting bits and symbols
tri = [0] * 3
for i in range(PSK8.total):
    PSK8.binary()
    tri[i % 3] = PSK8.bits[i]
    if (i % 3 + 1) == 3:
        if tri[0] == 0 and tri[1] == 0 and tri[2] == 0:
            PSK8.symbols.append(complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))

        elif tri[0] == 0 and tri[1] == 0 and tri[2] == 1:
            PSK8.symbols.append(complex(-1, 0))

        elif tri[0] == 0 and tri[1] == 1 and tri[2] == 1:
            PSK8.symbols.append(complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))

        elif tri[0] == 0 and tri[1] == 1 and tri[2] == 0:
            PSK8.symbols.append(complex(0, 1))

        elif tri[0] == 1 and tri[1] == 1 and tri[2] == 0:
            PSK8.symbols.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))

        elif tri[0] == 1 and tri[1] == 1 and tri[2] == 1:
            PSK8.symbols.append(complex(1, 0))

        elif tri[0] == 1 and tri[1] == 0 and tri[2] == 1:
            PSK8.symbols.append(complex(1 / math.sqrt(2), -1 / math.sqrt(2)))

        elif tri[0] == 1 and tri[1] == 0 and tri[2] == 0:
            PSK8.symbols.append(complex(0, -1))
print(4)

# print("8PSK Bits: " + str(PSK8.bits))
# print("8PSK Symb: " + str(PSK8.symbols))
# print()

# ----------------------------------------------------------------
# Set s0 and s1
# ----------------------------------------------------------------
BPSK.s = [[1, 1, 1],
          [-1, 1, 1],
          [1, 1, -1],
          [-1, 1, -1],
          [1, -1, 1],
          [-1, -1, 1],
          [1, -1, -1],
          [-1, -1, -1]]

QAM4.s = [[complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          [complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)]]

# 1, 1
PSK8.s = [[complex(1, 0), complex(1, 0), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(1, 0)],
          [complex(0, 1), complex(1, 0), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(1, 0)],
          [complex(-1, 0), complex(1, 0), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(1, 0)],
          [complex(0, -1), complex(1, 0), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(1, 0)],

          # 1, (1,j)
          [complex(1, 0), complex(1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(1, 1) / math.sqrt(2)],

          # 1, j
          [complex(1, 0), complex(1, 0), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(0, 1)],
          [complex(0, 1), complex(1, 0), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(0, 1)],
          [complex(-1, 0), complex(1, 0), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(0, 1)],
          [complex(0, -1), complex(1, 0), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(0, 1)],

          # 1, (-1,j)
          [complex(1, 0), complex(1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(-1, 1) / math.sqrt(2)],

          # 1, -1
          [complex(1, 0), complex(1, 0), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(-1, 0)],
          [complex(0, 1), complex(1, 0), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(-1, 0)],
          [complex(-1, 0), complex(1, 0), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(-1, 0)],
          [complex(0, -1), complex(1, 0), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(-1, 0)],

          # 1, (-1,-j)
          [complex(1, 0), complex(1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(-1, -1) / math.sqrt(2)],

          # 1, -j
          [complex(1, 0), complex(1, 0), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(0, -1)],
          [complex(0, 1), complex(1, 0), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(0, -1)],
          [complex(-1, 0), complex(1, 0), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(0, -1)],
          [complex(0, -1), complex(1, 0), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(0, -1)],

          # 1, (1,-j)
          [complex(1, 0), complex(1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 0), complex(1, -1) / math.sqrt(2)],

          # (1, j), 1
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 0)],

          # (1, j), (1,j)
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          # (1, j), j
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, 1)],

          # (1, j), (-1,j)
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          # (1, j), -1
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, 0)],

          # (1, j), (-1,-j)
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          # (1, j), -j
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(0, -1)],

          # (1, j), (1,-j)
          [complex(1, 0), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],

          # j, 1
          [complex(1, 0), complex(0, 1), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(1, 0)],
          [complex(0, 1), complex(0, 1), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(1, 0)],
          [complex(-1, 0), complex(0, 1), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(1, 0)],
          [complex(0, -1), complex(0, 1), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(1, 0)],

          # j, (1,j)
          [complex(1, 0), complex(0, 1), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(0, 1), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, 1), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(0, 1), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(1, 1) / math.sqrt(2)],

          # j, j
          [complex(1, 0), complex(0, 1), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(0, 1)],
          [complex(0, 1), complex(0, 1), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(0, 1)],
          [complex(-1, 0), complex(0, 1), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(0, 1)],
          [complex(0, -1), complex(0, 1), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(0, 1)],

          # j, (-1,j)
          [complex(1, 0), complex(0, 1), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(0, 1), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, 1), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(0, 1), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(-1, 1) / math.sqrt(2)],

          # j, -1
          [complex(1, 0), complex(0, 1), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(-1, 0)],
          [complex(0, 1), complex(0, 1), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(-1, 0)],
          [complex(-1, 0), complex(0, 1), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(-1, 0)],
          [complex(0, -1), complex(0, 1), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(-1, 0)],

          # j, (-1,-j)
          [complex(1, 0), complex(0, 1), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(0, 1), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, 1), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(0, 1), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(-1, -1) / math.sqrt(2)],

          # j, -j
          [complex(1, 0), complex(0, 1), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(0, -1)],
          [complex(0, 1), complex(0, 1), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(0, -1)],
          [complex(-1, 0), complex(0, 1), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(0, -1)],
          [complex(0, -1), complex(0, 1), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(0, -1)],

          # j, (1,-j)
          [complex(1, 0), complex(0, 1), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, 1), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(0, 1), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, 1), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, 1), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, 1), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(0, 1), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, 1), complex(1, -1) / math.sqrt(2)],

          # (-1, j), 1
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 0)],

          # (-1, j), (1,j)
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          # (-1, j), j
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, 1)],

          # (-1, j), (-1,j)
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          # (-1, j), -1
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, 0)],

          # (-1, j), (-1,-j)
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          # (-1, j), -j
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(0, -1)],

          # (-1, j), (1,-j)
          [complex(1, 0), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],

          # -1, 1
          [complex(1, 0), complex(-1, 0), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(1, 0)],
          [complex(0, 1), complex(-1, 0), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(1, 0)],
          [complex(-1, 0), complex(-1, 0), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(1, 0)],
          [complex(0, -1), complex(-1, 0), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(1, 0)],

          # -1, (1,j)
          [complex(1, 0), complex(-1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 0), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(1, 1) / math.sqrt(2)],

          # -1, j
          [complex(1, 0), complex(-1, 0), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(0, 1)],
          [complex(0, 1), complex(-1, 0), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(0, 1)],
          [complex(-1, 0), complex(-1, 0), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(0, 1)],
          [complex(0, -1), complex(-1, 0), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(0, 1)],

          # -1, (-1,j)
          [complex(1, 0), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(-1, 1) / math.sqrt(2)],

          # -1, -1
          [complex(1, 0), complex(-1, 0), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(-1, 0)],
          [complex(0, 1), complex(-1, 0), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(-1, 0)],
          [complex(-1, 0), complex(-1, 0), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(-1, 0)],
          [complex(0, -1), complex(-1, 0), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(-1, 0)],

          # -1, (-1,-j)
          [complex(1, 0), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(-1, -1) / math.sqrt(2)],

          # -1, -j
          [complex(1, 0), complex(-1, 0), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(0, -1)],
          [complex(0, 1), complex(-1, 0), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(0, -1)],
          [complex(-1, 0), complex(-1, 0), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(0, -1)],
          [complex(0, -1), complex(-1, 0), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(0, -1)],

          # -1, (1,-j)
          [complex(1, 0), complex(-1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, 0), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, 0), complex(1, -1) / math.sqrt(2)],

          # (-1, -j), 1
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],

          # (-1, -j), (1,j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          # (-1, -j), j
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],

          # (-1, -j), (-1,j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          # (-1, -j), -1
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],

          # (-1, -j), (-1,-j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          # (-1, -j), -j
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],

          # (-1, -j), (1,-j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],

          # -j, 1
          [complex(1, 0), complex(0, -1), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(1, 0)],
          [complex(0, 1), complex(0, -1), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(1, 0)],
          [complex(-1, 0), complex(0, -1), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(1, 0)],
          [complex(0, -1), complex(0, -1), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(1, 0)],

          # -j, (1,j)
          [complex(1, 0), complex(0, -1), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(0, -1), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, -1), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(0, -1), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(1, 1) / math.sqrt(2)],

          # -j, j
          [complex(1, 0), complex(0, -1), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(0, 1)],
          [complex(0, 1), complex(0, -1), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(0, 1)],
          [complex(-1, 0), complex(0, -1), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(0, 1)],
          [complex(0, -1), complex(0, -1), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(0, 1)],

          # -j, (-1,j)
          [complex(1, 0), complex(0, -1), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(0, -1), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, -1), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(0, -1), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(-1, 1) / math.sqrt(2)],

          # -j, -1
          [complex(1, 0), complex(0, -1), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(-1, 0)],
          [complex(0, 1), complex(0, -1), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(-1, 0)],
          [complex(-1, 0), complex(0, -1), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(-1, 0)],
          [complex(0, -1), complex(0, -1), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(-1, 0)],

          # -j, (-1,-j)
          [complex(1, 0), complex(0, -1), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(0, -1), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, -1), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(0, -1), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(-1, -1) / math.sqrt(2)],

          # -j, -j
          [complex(1, 0), complex(0, -1), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(0, -1)],
          [complex(0, 1), complex(0, -1), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(0, -1)],
          [complex(-1, 0), complex(0, -1), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(0, -1)],
          [complex(0, -1), complex(0, -1), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(0, -1)],

          # -j, (1,-j)
          [complex(1, 0), complex(0, -1), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(0, -1), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(0, -1), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(0, -1), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(0, -1), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(0, -1), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(0, -1), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(0, -1), complex(1, -1) / math.sqrt(2)],

          # (-1, -j), 1
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 0)],

          # (-1, -j), (1,j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, 1) / math.sqrt(2)],

          # (-1, -j), j
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(0, 1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, 1)],

          # (-1, -j), (-1,j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 1) / math.sqrt(2)],

          # (-1, -j), -1
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, 0)],

          # (-1, -j), (-1,-j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2)],

          # (-1, -j), -j
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(0, -1)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(0, -1)],

          # (-1, -j), (1,-j)
          [complex(1, 0), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, 1), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, 0), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(-1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(0, -1), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)],
          [complex(1, -1) / math.sqrt(2), complex(-1, -1) / math.sqrt(2), complex(1, -1) / math.sqrt(2)]]
print(5)

# ----------------------------------------------------------------
# Get Transmitted Bits and Symbols
# ----------------------------------------------------------------

# fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
# fig.subplots_adjust(hspace=0.001, wspace=0.001)
# axs = axs.ravel()
# BPSK
for k in range(-4, 16):
    BPSK.symErrorCount = 0
    BPSK.transmittedSymbols = [complex(1, 0), complex(1, 0)]
    BPSK.rt = []
    BPSK.delta = [[0.0] * BPSK.total for m in range(BPSK.M ** 3)]
    BPSK.alpha = [0.0] * BPSK.total
    BPSK.sigma = 1 / (math.sqrt((10 ** (k / 10)) * 2 * math.log(BPSK.M, 2)))

    for i in range(BPSK.total):
        for j in range(BPSK.M ** 3):
            BPSK.rt.append((BPSK.s[j][0] * BPSK.cStatic[0]) + (BPSK.s[j][1] * BPSK.cStatic[1]) + (
                    BPSK.s[j][2] * BPSK.cStatic[2]) + (
                                   BPSK.sigma * (complex(random.gauss(0, 1), random.gauss(0, 1)))))
            BPSK.delta[j][i] = abs(BPSK.rt[i] - ((BPSK.s[j][0] * BPSK.cStatic[0]) + (BPSK.s[j][1] * BPSK.cStatic[1]) + (
                    BPSK.s[j][2] * BPSK.cStatic[2]))) ** 2
        temp = math.inf

        for l in range(BPSK.M ** 3):
            if temp >= BPSK.delta[l][i]:
                BPSK.alpha[i] = l
                temp = BPSK.delta[l][i]

    for m in range(len(BPSK.alpha)):
        BPSK.transmittedSymbols.append(BPSK.s[BPSK.alpha[m]][0])

    BPSK.transmittedSymbols.pop()
    BPSK.transmittedSymbols.pop()
    for x in range(len(BPSK.transmittedSymbols)):
        if BPSK.transmittedSymbols[x] != BPSK.symbols[x]:
            BPSK.symErrorCount += 1

    # x = []
    # y = []
    #
    # for l1 in range(0, len(BPSK.rt)):
    #     x.append(BPSK.rt[l1].real)
    #     y.append(BPSK.rt[l1].imag)
    # for i in range(-4, 16):
    #     axs[i].scatter(x, y, marker='.',  label="Eb/No="+str(i), color='k',  alpha = 0.01)
    #     axs[i].legend(loc="upper right", framealpha=0)

    BPSK.SER.append(BPSK.symErrorCount / BPSK.total)

# print("Delta\n", len(BPSK.transmittedSymbols))
# print("\n\nAlpha\n", BPSK.s)
# print("\n\nAlpha length\n", len(BPSK.s))
#
# # print("\n\nSymbols BPSK\n", BPSK.symbols)
# print("\n\nSymbols BPSK Length\n", len(BPSK.symbols))
#
# print("\n\nSER\n", BPSK.SER)
print(6)

# 4QAM
for k in range(-4, 16):
    QAM4.symErrorCount = 0
    QAM4.transmittedSymbols = [complex(1, 0), complex(1, 0)]
    QAM4.rt = []
    QAM4.delta = [[0.0] * int(QAM4.total / 2) for m in range(QAM4.M ** 3)]
    QAM4.alpha = [0.0] * int(QAM4.total / 2)
    QAM4.sigma = 1 / (math.sqrt((10 ** (k / 10)) * 2 * math.log(QAM4.M, 2)))

    for i in range(int(QAM4.total / 2)):
        for j in range(QAM4.M ** 3):
            QAM4.rt.append((QAM4.s[j][0] * QAM4.cStatic[0]) + (QAM4.s[j][1] * QAM4.cStatic[1]) + (
                    QAM4.s[j][2] * QAM4.cStatic[2]) + (
                                   QAM4.sigma * (complex(random.gauss(0, 1), random.gauss(0, 1)))))
            QAM4.delta[j][i] = abs(QAM4.rt[i] - ((QAM4.s[j][0] * QAM4.cStatic[0]) + (QAM4.s[j][1] * QAM4.cStatic[1]) + (
                    QAM4.s[j][2] * QAM4.cStatic[2]))) ** 2
        temp = math.inf

        for l in range(QAM4.M ** 3):
            if temp >= QAM4.delta[l][i]:
                QAM4.alpha[i] = l
                temp = QAM4.delta[l][i]

    for m in range(len(QAM4.alpha)):
        QAM4.transmittedSymbols.append(QAM4.s[QAM4.alpha[m]][0])

    QAM4.transmittedSymbols.pop(0)
    QAM4.transmittedSymbols.pop(0)
    for p in range(0, int(QAM4.total / 2)):
        if QAM4.transmittedSymbols[p] == complex(1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("1", 'yellow'))
            QAM4.transmittedBits.append(0)
            QAM4.transmittedBits.append(0)
        elif QAM4.transmittedSymbols[p] == complex(-1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("2", 'yellow'))
            QAM4.transmittedBits.append(0)
            QAM4.transmittedBits.append(1)
        elif QAM4.transmittedSymbols[p] == complex(-1 / math.sqrt(2), -1 / math.sqrt(2)):
            # print(colored("3", 'yellow'))
            QAM4.transmittedBits.append(1)
            QAM4.transmittedBits.append(1)
        else:
            # print(colored("4", 'yellow'))
            QAM4.transmittedBits.append(1)
            QAM4.transmittedBits.append(0)

    for n in range(0, len(QAM4.bits)):
        if QAM4.bits[n] != QAM4.transmittedBits[n]:
            QAM4.bitErrorCount += 1

    for x in range(len(QAM4.transmittedSymbols)):
        if QAM4.transmittedSymbols[x] != QAM4.symbols[x]:
            QAM4.symErrorCount += 1

    # x = []
    # y = []
    #
    # for l1 in range(0, len(QAM4.rt)):
    #     x.append(QAM4.rt[l1].real)
    #     y.append(QAM4.rt[l1].imag)
    # for i in range(-4, 16):
    #     axs[i].scatter(x, y, marker='.',  label="Eb/No="+str(i), color='k',  alpha = 0.01)
    #     axs[i].legend(loc="upper right", framealpha=0)

    QAM4.BER.append(QAM4.bitErrorCount / QAM4.total)
    QAM4.SER.append(QAM4.symErrorCount / (QAM4.total / 2))
#
# print("Delta\n", len(QAM4.transmittedSymbols))
# print("\n\nAlpha\n", QAM4.s)
# print("\n\nAlpha length\n", len(QAM4.alpha))
#
# # print("\n\nSymbols QAM4\n", QAM4.symbols)
# print("\n\nSymbols QAM4 Length\n", len(QAM4.symbols))
#
# print("\n\nBER\n", QAM4.BER)
print(7)

# 8PSK
for k in range(-4, 16):
    PSK8.symErrorCount = 0
    PSK8.transmittedSymbols = [complex(1, 0), complex(1, 0)]
    PSK8.rt = []
    PSK8.delta = [[0.0] * int(PSK8.total / 3) for m in range(PSK8.M ** 3)]
    PSK8.alpha = [0.0] * int(PSK8.total / 3)
    PSK8.sigma = 1 / (math.sqrt((10 ** (k / 10)) * 2 * math.log(PSK8.M, 2)))

    for i in range(int(PSK8.total / 3)):
        for j in range(PSK8.M ** 3):
            PSK8.rt.append((PSK8.s[j][0] * PSK8.cStatic[0]) + (PSK8.s[j][1] * PSK8.cStatic[1]) + (
                    PSK8.s[j][2] * PSK8.cStatic[2]) + (
                                   PSK8.sigma * (complex(random.gauss(0, 1), random.gauss(0, 1)))))
            PSK8.delta[j][i] = abs(PSK8.rt[i] - ((PSK8.s[j][0] * PSK8.cStatic[0]) + (PSK8.s[j][1] * PSK8.cStatic[1]) + (
                    PSK8.s[j][2] * PSK8.cStatic[2]))) ** 2
        temp = math.inf

        for l in range(PSK8.M ** 3):
            if temp >= PSK8.delta[l][i]:
                PSK8.alpha[i] = l
                temp = PSK8.delta[l][i]

    for m in range(len(PSK8.alpha)):
        PSK8.transmittedSymbols.append(PSK8.s[PSK8.alpha[m]][0])

    PSK8.transmittedSymbols.pop(0)
    PSK8.transmittedSymbols.pop(0)
    for p in range(0, int(PSK8.total / 3)):
        # print("IN")
        if PSK8.transmittedSymbols[p] == complex(1, 0):
            # print(colored("1", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
        elif PSK8.transmittedSymbols[p] == complex(1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("2", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[p] == complex(0, 1):
            # print(colored("3", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[p] == complex(-1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("4", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
        elif PSK8.transmittedSymbols[p] == complex(-1, 0):
            # print(colored("5", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
        elif PSK8.transmittedSymbols[p] == complex(-1 / math.sqrt(2), -1 / math.sqrt(2)):
            # print(colored("6", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[p] == complex(0, -1):
            # print(colored("7", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[p] == complex(1 / math.sqrt(2), -1 / math.sqrt(2)):
            # print(colored("8", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
        else:
            print(colored("ERROR in Sym->Bits Transform", 'red'))

    for n in range(0, len(PSK8.bits)):
        if PSK8.bits[n] != PSK8.transmittedBits[n]:
            PSK8.bitErrorCount += 1

    for x in range(len(PSK8.transmittedSymbols)):
        if PSK8.transmittedSymbols[x] != PSK8.symbols[x]:
            PSK8.symErrorCount += 1

    # x = []
    # y = []
    #
    # for l1 in range(0, len(PSK8.rt)):
    #     x.append(PSK8.rt[l1].real)
    #     y.append(PSK8.rt[l1].imag)
    # for i in range(-4, 16):
    #     axs[i].scatter(x, y, marker='.',  label="Eb/No="+str(i), color='k',  alpha = 0.01)
    #     axs[i].legend(loc="upper right", framealpha=0)

    PSK8.BER.append(PSK8.bitErrorCount / PSK8.total)
    PSK8.SER.append(PSK8.symErrorCount / (PSK8.total / 3))

# print("Delta\n", len(PSK8.transmittedSymbols))
# print("\n\nAlpha\n", PSK8.s)
# print("\n\nAlpha length\n", len(PSK8.alpha))
#
# print("\n\nSymbols PSK8\n", PSK8.symbols)
# print("\n\nSymbols PSK8 Length\n", len(PSK8.symbols))

# print("\n\nBER\n", PSK8.BER)
print(8)

x = []
for i in range(-4, 16):
    x.append(i)
plt.semilogy(x, BPSK.SER, 'r-', label="BPSK BER")
plt.semilogy(x, QAM4.BER, 'k-', label="4QAM BER")
plt.semilogy(x, PSK8.BER, 'b-', label="8PSK BER")

plt.xlabel("Eb/No")
plt.ylabel("Bit Error Rate (BER) for Static CIR")
plt.legend()
plt.show()
print(9)
