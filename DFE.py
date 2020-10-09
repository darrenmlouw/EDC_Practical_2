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

uniform = question_1.PRNG()
normal = question_2.GRNG()


class Multipath:
    def __init__(self, bits, numM):
        self.N = 200
        self.rt = []  # [[0 for x in range(200)] for y in range(15)]
        self.s = []
        self.delta1 = []
        self.delta2 = []
        self.delta3 = []
        self.delta4 = []
        self.delta5 = []
        self.delta6 = []
        self.delta7 = []
        self.delta8 = []
        # self.cStatic = [complex(0.89, 0.92), complex(0.42, 0.37), complex(0.19, 0.12)]
        self.cStatic = [complex(0.89, 0.92), complex(0.42, 0.37), complex(0.19, 0.12)]
        # self.cStatic = [complex(1, 1), complex(0, 0), complex(0, 0)]
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
        # self.cDynamic = [complex(normal.randomNormal(), normal.randomNormal())/(2*math.sqrt(3)), complex(normal.randomNormal(), normal.randomNormal())/(2*math.sqrt(3)), complex(normal.randomNormal(), normal.randomNormal())/(2*math.sqrt(3))]
        self.cDynamic = [complex(random.gauss(0, 1), random.gauss(0, 1)) / (2 * math.sqrt(3)),
                         complex(random.gauss(0, 1), random.gauss(0, 1)) / (2 * math.sqrt(3)),
                         complex(random.gauss(0, 1), random.gauss(0, 1)) / (2 * math.sqrt(3))]


random.gauss(0, 1)

# ----------------------------------------------------------------
# Initialize
# ----------------------------------------------------------------
BPSK = Multipath(200000, 2)
QAM4 = Multipath(400000, 4)
PSK8 = Multipath(600000, 8)
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

# print("8PSK Bits: " + str(PSK8.bits))
# print("8PSK Symb: " + str(PSK8.symbols))
# print()
# ----------------------------------------------------------------
# Set s0 and s1
# ----------------------------------------------------------------
BPSK.s.append(complex(1, 0))
BPSK.s.append(complex(1, 0))
BPSK.s.extend(BPSK.symbols)

QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
QAM4.s.extend(QAM4.symbols)

PSK8.s.append(complex(1, 0))
PSK8.s.append(complex(1, 0))
PSK8.s.extend(PSK8.symbols)

# print(BPSK.s)
# print(QAM4.s)
# print(PSK8.s)
# print("Length: " + str(len(BPSK.s)))
# print("Length: " + str(len(QAM4.s)))
# print("Length: " + str(len(PSK8.s)))
# ----------------------------------------------------------------
# Get Transmitted Bits and Symbols
# ----------------------------------------------------------------

fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
fig.subplots_adjust(hspace=0.001, wspace=0.001)
axs = axs.ravel()

for i in range(0, 16):
    BPSK.symErrorCount = 0
    BPSK.transmittedSymbols = [complex(1, 0), complex(1, 0)]
    BPSK.rt = []
    BPSK.delta1 = []
    BPSK.delta2 = []
    BPSK.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log(BPSK.M, 2)))

    for j in range(0, BPSK.total):
        BPSK.rt.append((BPSK.s[j + 2] * BPSK.cStatic[0]) + (BPSK.s[j + 1] * BPSK.cStatic[1]) + (
                BPSK.s[j] * BPSK.cStatic[2]) + BPSK.sigma * (
                               complex(random.gauss(0, 1), random.gauss(0, 1)) / math.sqrt(2)))

        BPSK.delta1.append(pow(abs(
            BPSK.rt[j] - (((1) * BPSK.cStatic[0]) + (BPSK.s[j + 1] * BPSK.cStatic[1]) + (BPSK.s[j] * BPSK.cStatic[2]))),
            2))  # s/trans
        BPSK.delta2.append(pow(abs(BPSK.rt[j] - (
                ((-1) * BPSK.cStatic[0]) + (BPSK.s[j + 1] * BPSK.cStatic[1]) + (BPSK.s[j] * BPSK.cStatic[2]))),
                               2))  # s/trans

        if BPSK.delta1[j] < BPSK.delta2[j]:
            BPSK.transmittedSymbols.append(1)
        else:
            BPSK.transmittedSymbols.append(-1)

        # print("hereeede")
        # print(BPSK.s)
        # print(BPSK.transmittedSymbols)

        # if BPSK.s[j] != BPSK.transmittedSymbols[j]:
        #     BPSK.symErrorCount += 1
        #
        # print(colored(BPSK.symErrorCount, 'yellow'))

    for k in range(0, len(BPSK.s)):
        if BPSK.s[k] != BPSK.transmittedSymbols[k]:
            BPSK.symErrorCount += 1

        # print(colored(BPSK.transmittedSymbols, 'blue'))

    x = []
    y = []

    for l1 in range(0, len(BPSK.rt)):
        x.append(BPSK.rt[l1].real)
        y.append(BPSK.rt[l1].imag)

    axs[i].scatter(x, y, marker='.',  label="Eb/No="+str(i), color='k',  alpha = 0.05)
    axs[i].legend(loc="lower right", framealpha=0)

    BPSK.SER.append(BPSK.symErrorCount / BPSK.total)
    # print(BPSK.SER)


fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
fig.subplots_adjust(hspace=0.001, wspace=0.001)
axs = axs.ravel()

# fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
# fig.subplots_adjust(hspace=0.001, wspace=0.001)
# axs = axs.ravel()

# print("4QAM")
for i in range(0, 16):
    QAM4.symErrorCount = 0
    QAM4.transmittedSymbols = [complex(1 / math.sqrt(2), 1 / math.sqrt(2)), complex(1 / math.sqrt(2), 1 / math.sqrt(2))]
    QAM4.rt = []
    QAM4.delta1 = []
    QAM4.delta2 = []
    QAM4.delta3 = []
    QAM4.delta4 = []
    QAM4.transmittedBits = []
    QAM4.bitErrorCount = 0
    QAM4.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log(QAM4.M, 2)))
    for j in range(0, int(QAM4.total / 2)):
        QAM4.rt.append(
            (QAM4.s[j + 2] * QAM4.cStatic[0]) + (QAM4.s[j + 1] * QAM4.cStatic[1]) + (QAM4.s[j] * QAM4.cStatic[2]) + (
                    QAM4.sigma * (complex(random.gauss(0, 1), random.gauss(0, 1)) / math.sqrt(2))))

        QAM4.delta1.append(pow(abs(QAM4.rt[j] - (((complex(1 / math.sqrt(2), 1 / math.sqrt(2))) * QAM4.cStatic[0]) + (
                QAM4.s[j + 1] * QAM4.cStatic[1]) + (QAM4.s[j] * QAM4.cStatic[2]))), 2))
        QAM4.delta2.append(pow(abs(QAM4.rt[j] - (((complex(-1 / math.sqrt(2), 1 / math.sqrt(2))) * QAM4.cStatic[0]) + (
                QAM4.s[j + 1] * QAM4.cStatic[1]) + (QAM4.s[j] * QAM4.cStatic[2]))), 2))
        QAM4.delta3.append(pow(abs(QAM4.rt[j] - (((complex(-1 / math.sqrt(2), -1 / math.sqrt(2))) * QAM4.cStatic[0]) + (
                QAM4.s[j + 1] * QAM4.cStatic[1]) + (QAM4.s[j] * QAM4.cStatic[2]))), 2))
        QAM4.delta4.append(pow(abs(QAM4.rt[j] - (((complex(1 / math.sqrt(2), -1 / math.sqrt(2))) * QAM4.cStatic[0]) + (
                QAM4.s[j + 1] * QAM4.cStatic[1]) + (QAM4.s[j] * QAM4.cStatic[2]))), 2))

        # print(colored("DELTAS", 'blue'))
        # print(QAM4.delta1)
        # print(QAM4.delta2)
        # print(QAM4.delta3)
        # print(QAM4.delta4)

        if (QAM4.delta1[j] < QAM4.delta2[j]) and (QAM4.delta1[j] < QAM4.delta3[j]) and (
                QAM4.delta1[j] < QAM4.delta4[j]):
            # print(colored("1", 'yellow'))
            QAM4.transmittedSymbols.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
        elif (QAM4.delta2[j] < QAM4.delta1[j]) and (QAM4.delta2[j] < QAM4.delta3[j]) and (
                QAM4.delta2[j] < QAM4.delta4[j]):
            # print(colored("2", 'yellow'))
            QAM4.transmittedSymbols.append(complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))
        elif (QAM4.delta3[j] < QAM4.delta1[j]) and (QAM4.delta3[j] < QAM4.delta2[j]) and (
                QAM4.delta3[j] < QAM4.delta4[j]):
            # print(colored("3", 'yellow'))
            QAM4.transmittedSymbols.append(complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))
        elif (QAM4.delta4[j] < QAM4.delta1[j]) and (QAM4.delta4[j] < QAM4.delta2[j]) and (
                QAM4.delta4[j] < QAM4.delta3[j]):
            # print(colored("4", 'yellow'))
            QAM4.transmittedSymbols.append(complex(1 / math.sqrt(2), -1 / math.sqrt(2)))
        else:
            print("Error 4QAM")

        # if QAM4.s[j] != QAM4.transmittedSymbols[j] and j%2==0:
        #     QAM4.symErrorCount += 1

    QAM4.transmittedSymbols.pop(0)
    QAM4.transmittedSymbols.pop(0)
    for j in range(0, int(QAM4.total / 2)):
        if QAM4.transmittedSymbols[j] == complex(1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("1", 'yellow'))
            QAM4.transmittedBits.append(0)
            QAM4.transmittedBits.append(0)
        elif QAM4.transmittedSymbols[j] == complex(-1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("2", 'yellow'))
            QAM4.transmittedBits.append(0)
            QAM4.transmittedBits.append(1)
        elif QAM4.transmittedSymbols[j] == complex(-1 / math.sqrt(2), -1 / math.sqrt(2)):
            # print(colored("3", 'yellow'))
            QAM4.transmittedBits.append(1)
            QAM4.transmittedBits.append(1)
        else:
            # print(colored("4", 'yellow'))
            QAM4.transmittedBits.append(1)
            QAM4.transmittedBits.append(0)

    for k in range(0, len(QAM4.bits)):
        if QAM4.bits[k] != QAM4.transmittedBits[k]:
            QAM4.bitErrorCount += 1

    x = []
    y = []

    for l1 in range(0, len(QAM4.rt)):
        x.append(QAM4.rt[l1].real)
        y.append(QAM4.rt[l1].imag)

    axs[i].scatter(x, y, marker=".", alpha = 0.01, label="Eb/No="+str(i), color='k')
    axs[i].legend(loc="upper right", framealpha=0)

    QAM4.BER.append(QAM4.bitErrorCount / QAM4.total)

    QAM4.SER.append(QAM4.symErrorCount / (QAM4.total / 2))

    # print(QAM4.SER)

plt.show()


fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
fig.subplots_adjust(hspace=0.001, wspace=0.001)
axs = axs.ravel()

for i in range(0, 16):
    PSK8.symErrorCount = 0
    PSK8.transmittedSymbols = [complex(1, 0), complex(1, 0)]
    PSK8.rt = []
    PSK8.delta1 = []
    PSK8.delta2 = []
    PSK8.delta3 = []
    PSK8.delta4 = []
    PSK8.delta5 = []
    PSK8.delta6 = []
    PSK8.delta7 = []
    PSK8.delta8 = []
    PSK8.transmittedBits = []
    PSK8.bitErrorCount = 0
    PSK8.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log(PSK8.M, 2)))
    for j in range(0, int(PSK8.total / 3)):
        # print(colored("Start", 'green'))
        # print("Sigma: " + str(PSK8.sigma))
        PSK8.rt.append(
            (PSK8.s[j + 2] * PSK8.cStatic[0]) + (PSK8.s[j + 1] * PSK8.cStatic[1]) + (PSK8.s[j] * PSK8.cStatic[2]) + (
                    PSK8.sigma * (complex(random.gauss(0, 1), random.gauss(0, 1)) / math.sqrt(2))))

        PSK8.delta1.append(pow(abs(PSK8.rt[j] - (
                ((complex(1, 0)) * PSK8.cStatic[0]) + (PSK8.s[j + 1] * PSK8.cStatic[1]) + (
                PSK8.s[j] * PSK8.cStatic[2]))), 2))
        PSK8.delta2.append(pow(abs(PSK8.rt[j] - (((complex(1 / math.sqrt(2), 1 / math.sqrt(2))) * PSK8.cStatic[0]) + (
                PSK8.s[j + 1] * PSK8.cStatic[1]) + (PSK8.s[j] * PSK8.cStatic[2]))), 2))
        PSK8.delta3.append(pow(abs(PSK8.rt[j] - (
                ((complex(0, 1)) * PSK8.cStatic[0]) + (PSK8.s[j + 1] * PSK8.cStatic[1]) + (
                PSK8.s[j] * PSK8.cStatic[2]))), 2))
        PSK8.delta4.append(pow(abs(PSK8.rt[j] - (((complex(-1 / math.sqrt(2), 1 / math.sqrt(2))) * PSK8.cStatic[0]) + (
                PSK8.s[j + 1] * PSK8.cStatic[1]) + (PSK8.s[j] * PSK8.cStatic[2]))), 2))
        PSK8.delta5.append(pow(abs(PSK8.rt[j] - (
                ((complex(-1, 0)) * PSK8.cStatic[0]) + (PSK8.s[j + 1] * PSK8.cStatic[1]) + (
                PSK8.s[j] * PSK8.cStatic[2]))), 2))
        PSK8.delta6.append(pow(abs(PSK8.rt[j] - (((complex(-1 / math.sqrt(2), -1 / math.sqrt(2))) * PSK8.cStatic[0]) + (
                PSK8.s[j + 1] * PSK8.cStatic[1]) + (PSK8.s[j] * PSK8.cStatic[2]))), 2))
        PSK8.delta7.append(pow(abs(PSK8.rt[j] - (
                ((complex(0, -1)) * PSK8.cStatic[0]) + (PSK8.s[j + 1] * PSK8.cStatic[1]) + (
                PSK8.s[j] * PSK8.cStatic[2]))), 2))
        PSK8.delta8.append(pow(abs(PSK8.rt[j] - (((complex(1 / math.sqrt(2), -1 / math.sqrt(2))) * PSK8.cStatic[0]) + (
                PSK8.s[j + 1] * PSK8.cStatic[1]) + (PSK8.s[j] * PSK8.cStatic[2]))), 2))

        # print(colored("DELTAS", 'blue'))
        # print(PSK8.delta1[j])
        # print(PSK8.delta2[j])
        # print(PSK8.delta3[j])
        # print(PSK8.delta4[j])
        # print(PSK8.delta5[j])
        # print(PSK8.delta6[j])
        # print(PSK8.delta7[j])
        # print(PSK8.delta8[j])

        if (PSK8.delta1[j] < PSK8.delta2[j]) and (PSK8.delta1[j] < PSK8.delta3[j]) and (
                PSK8.delta1[j] < PSK8.delta4[j]) and (PSK8.delta1[j] < PSK8.delta5[j]) and (
                PSK8.delta1[j] < PSK8.delta6[j]) and (PSK8.delta1[j] < PSK8.delta7[j]) and (
                PSK8.delta1[j] < PSK8.delta8[j]):
            # print(colored("1", 'yellow'))
            PSK8.transmittedSymbols.append(complex(1, 0))
        elif (PSK8.delta2[j] < PSK8.delta1[j]) and (PSK8.delta2[j] < PSK8.delta3[j]) and (
                PSK8.delta2[j] < PSK8.delta4[j]) and (PSK8.delta2[j] < PSK8.delta5[j]) and (
                PSK8.delta2[j] < PSK8.delta6[j]) and (PSK8.delta2[j] < PSK8.delta7[j]) and (
                PSK8.delta2[j] < PSK8.delta8[j]):
            # print(colored("2", 'yellow'))
            PSK8.transmittedSymbols.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
        elif (PSK8.delta3[j] < PSK8.delta1[j]) and (PSK8.delta3[j] < PSK8.delta2[j]) and (
                PSK8.delta3[j] < PSK8.delta4[j]) and (PSK8.delta3[j] < PSK8.delta5[j]) and (
                PSK8.delta3[j] < PSK8.delta6[j]) and (PSK8.delta3[j] < PSK8.delta7[j]) and (
                PSK8.delta3[j] < PSK8.delta8[j]):
            # print(colored("3", 'yellow'))
            PSK8.transmittedSymbols.append(complex(0, 1))
        elif (PSK8.delta4[j] < PSK8.delta1[j]) and (PSK8.delta4[j] < PSK8.delta2[j]) and (
                PSK8.delta4[j] < PSK8.delta3[j]) and (PSK8.delta4[j] < PSK8.delta5[j]) and (
                PSK8.delta4[j] < PSK8.delta6[j]) and (PSK8.delta4[j] < PSK8.delta7[j]) and (
                PSK8.delta4[j] < PSK8.delta8[j]):
            # print(colored("4", 'yellow'))
            PSK8.transmittedSymbols.append(complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))
        elif (PSK8.delta5[j] < PSK8.delta1[j]) and (PSK8.delta5[j] < PSK8.delta2[j]) and (
                PSK8.delta5[j] < PSK8.delta3[j]) and (PSK8.delta5[j] < PSK8.delta4[j]) and (
                PSK8.delta5[j] < PSK8.delta6[j]) and (PSK8.delta5[j] < PSK8.delta7[j]) and (
                PSK8.delta5[j] < PSK8.delta8[j]):
            # print(colored("5", 'yellow'))
            PSK8.transmittedSymbols.append(complex(-1, 0))
        elif (PSK8.delta6[j] < PSK8.delta1[j]) and (PSK8.delta6[j] < PSK8.delta2[j]) and (
                PSK8.delta6[j] < PSK8.delta3[j]) and (PSK8.delta6[j] < PSK8.delta4[j]) and (
                PSK8.delta6[j] < PSK8.delta5[j]) and (PSK8.delta6[j] < PSK8.delta7[j]) and (
                PSK8.delta6[j] < PSK8.delta8[j]):
            # print(colored("6", 'yellow'))
            PSK8.transmittedSymbols.append(complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))
        elif (PSK8.delta7[j] < PSK8.delta1[j]) and (PSK8.delta7[j] < PSK8.delta2[j]) and (
                PSK8.delta7[j] < PSK8.delta3[j]) and (PSK8.delta7[j] < PSK8.delta4[j]) and (
                PSK8.delta7[j] < PSK8.delta5[j]) and (PSK8.delta7[j] < PSK8.delta6[j]) and (
                PSK8.delta7[j] < PSK8.delta8[j]):
            # print(colored("7", 'yellow'))
            PSK8.transmittedSymbols.append(complex(0, -1))
        elif (PSK8.delta8[j] < PSK8.delta1[j]) and (PSK8.delta8[j] < PSK8.delta2[j]) and (
                PSK8.delta8[j] < PSK8.delta3[j]) and (PSK8.delta8[j] < PSK8.delta4[j]) and (
                PSK8.delta8[j] < PSK8.delta5[j]) and (PSK8.delta8[j] < PSK8.delta6[j]) and (
                PSK8.delta8[j] < PSK8.delta7[j]):
            # print(colored("8", 'yellow'))
            PSK8.transmittedSymbols.append(complex(1 / math.sqrt(2), -1 / math.sqrt(2)))
        else:
            print(colored("ERROR in Delta Check", 'red'))

        if PSK8.s[j] != PSK8.transmittedSymbols[j]:
            PSK8.symErrorCount += 1

        # print(colored("TRANS: ", 'green'))
        # print(PSK8.bits[j])
        # print(PSK8.symbols[j])
        # print(PSK8.transmittedSymbols[j])

    PSK8.transmittedSymbols.pop(0)
    PSK8.transmittedSymbols.pop(0)

    # print("HERER")
    for j in range(0, int(PSK8.total / 3)):
        # print("IN")
        if PSK8.transmittedSymbols[j] == complex(1, 0):
            # print(colored("1", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
        elif PSK8.transmittedSymbols[j] == complex(1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("2", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[j] == complex(0, 1):
            # print(colored("3", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[j] == complex(-1 / math.sqrt(2), 1 / math.sqrt(2)):
            # print(colored("4", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(1)
        elif PSK8.transmittedSymbols[j] == complex(-1, 0):
            # print(colored("5", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
        elif PSK8.transmittedSymbols[j] == complex(-1 / math.sqrt(2), -1 / math.sqrt(2)):
            # print(colored("6", 'blue'))
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[j] == complex(0, -1):
            # print(colored("7", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(0)
        elif PSK8.transmittedSymbols[j] == complex(1 / math.sqrt(2), -1 / math.sqrt(2)):
            # print(colored("8", 'blue'))
            PSK8.transmittedBits.append(1)
            PSK8.transmittedBits.append(0)
            PSK8.transmittedBits.append(1)
        else:
            print(colored("ERROR in Sym->Bits Transform", 'red'))

        # print(PSK8.transmittedBits[j])

        if PSK8.bits[j] != PSK8.transmittedBits[j]:
            PSK8.bitErrorCount += 1

    x = []
    y = []

    for l1 in range(0, len(PSK8.rt)):
        x.append(PSK8.rt[l1].real)
        y.append(PSK8.rt[l1].imag)

    axs[i].scatter(x, y, marker=".", alpha=0.01, label="Eb/No="+str(i), color='k')
    axs[i].legend(loc="upper right", framealpha=0)

    # print(colored("NEXT", 'blue'))
    # print(PSK8.SER)
    # print(PSK8.BER)

    PSK8.BER.append(PSK8.bitErrorCount / PSK8.total)

    PSK8.SER.append(PSK8.symErrorCount / (PSK8.total / 3))

    # print(PSK8.SER)

plt.show()


x = []
for i in range(0, 16):
    x.append(i)
plt.semilogy(x, BPSK.SER, 'r-', label="BPSK BER")
# plt.semilogy(x, QAM4.SER, 'k-', label="4QAM SER")
plt.semilogy(x, QAM4.BER, 'k-', label="4QAM BER")
# plt.semilogy(x, PSK8.SER, 'b-', label="8PSK SER")
plt.semilogy(x, PSK8.BER, 'b-', label="8PSK BER")

# print(BPSK.SER)
# print(BPSK.rt)
# print(BPSK.transmittedSymbols)

# ----------------------------------------------------------------
# Calculate Deltas
# ----------------------------------------------------------------
# for i in range(0, 200):
#     BPSK.delta1.append(abs())
#     BPSK.delta2.append()
#
#     QAM4.delta1.append()
#     QAM4.delta2.append()
#
#     PSK8.delta1.append()
#     PSK8.delta2.append()

# BPSK.newDynamic()
# print(BPSK.cStatic)

plt.xlabel("Eb/No")
plt.ylabel("Bit Error Rate (BER) for Static CIR")
plt.legend()
plt.show()
# print(BPSK.cDynamic)
