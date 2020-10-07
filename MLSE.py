import question_1
import question_2
import question_3
import numpy as np
import math
import cmath
import matplotlib.pyplot as plt
import time
from termcolor import colored, cprint
import random

uniformNumber = question_1.PRNG()
noiseNumber = question_2.GRNG()


class MLSE:
    def __init__(self, bits, numM):
        self.N = 200
        self.rt = []  # [[0 for x in range(200)] for y in range(15)]
        self.s = []
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
BPSK = MLSE(2000, 2)
QAM4 = MLSE(4000, 4)
PSK8 = MLSE(6000, 8)
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

print("BPSK Bits: " + str(BPSK.bits))
print("BPSK Symb: " + str(BPSK.symbols))
print()

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

print("4QAM Bits: " + str(QAM4.bits))
print("4QAM Symb: " + str(QAM4.symbols))
print()

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

print("8PSK Bits: " + str(PSK8.bits))
print("8PSK Symb: " + str(PSK8.symbols))
print()

# ----------------------------------------------------------------
# Set s0 and s1
# ----------------------------------------------------------------
BPSK.s.append(complex(1, 0))
BPSK.s.append(complex(1, 0))
BPSK.s.extend(BPSK.symbols)
BPSK.s.append(complex(1, 0))
BPSK.s.append(complex(1, 0))

QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
QAM4.s.extend(QAM4.symbols)
QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))

PSK8.s.append(complex(1, 0))
PSK8.s.append(complex(1, 0))
PSK8.s.extend(PSK8.symbols)
PSK8.s.append(complex(1, 0))
PSK8.s.append(complex(1, 0))

print(BPSK.s)
print(QAM4.s)
print(PSK8.s)
print("Length: " + str(len(BPSK.s)))
print("Length: " + str(len(QAM4.s)))
print("Length: " + str(len(PSK8.s)))