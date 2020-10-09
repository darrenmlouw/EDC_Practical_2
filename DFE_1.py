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


# class to store relevant information regarding the DFE
class Multipath:
    def __init__(self, bits, numM):
        self.N = 200
        self.rt = []
        self.s = []
        self.delta1 = []
        self.delta2 = []
        self.delta3 = []
        self.delta4 = []
        self.delta5 = []
        self.delta6 = []
        self.delta7 = []
        self.delta8 = []
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
        self.BER = [0] * 16
        self.BERn = [0] * 16
        self.BERd = [0] * 16
        self.SER = [0] * 16
        self.SERn = [0] * 16
        self.SERd = [0] * 16

    def binary(self):
        temp = random.random()
        if temp > 0.5:
            self.bits.append(1)
        else:
            self.bits.append(0)

    def newDynamic(self):
        self.cDynamic = [complex(random.gauss(0, 1), random.gauss(0, 1)) / (math.sqrt(6)),
                         complex(random.gauss(0, 1), random.gauss(0, 1)) / (math.sqrt(6)),
                         complex(random.gauss(0, 1), random.gauss(0, 1)) / (math.sqrt(6))]


random.gauss(0, 1)

# ----------------------------------------------------------------
# Initialize
# ----------------------------------------------------------------
BPSK = Multipath(200, 2)
QAM4 = Multipath(400, 4)
PSK8 = Multipath(600, 8)
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

QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
QAM4.s.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
QAM4.s.extend(QAM4.symbols)

PSK8.s.append(complex(1, 0))
PSK8.s.append(complex(1, 0))
PSK8.s.extend(PSK8.symbols)

print(BPSK.s)
print(QAM4.s)
print(PSK8.s)
print("Length: " + str(len(BPSK.s)))
print("Length: " + str(len(QAM4.s)))
print("Length: " + str(len(PSK8.s)))
# ----------------------------------------------------------------
# Get Transmitted Bits and Symbols
# ----------------------------------------------------------------


# fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
# fig.subplots_adjust(hspace=0.001, wspace=0.001)
# axs = axs.ravel()
for m in range(0, 500):
    print(m)
    BPSK.newDynamic()
    for i in range(0, 16):
        BPSK.symErrorCount = 0
        BPSK.transmittedSymbols = [complex(1, 0), complex(1, 0)]
        BPSK.rt = []
        BPSK.delta1 = []
        BPSK.delta2 = []
        BPSK.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log(BPSK.M, 2)))

        for j in range(0, BPSK.total):
            BPSK.rt.append((BPSK.s[j + 2] * BPSK.cDynamic[0]) + (BPSK.s[j + 1] * BPSK.cDynamic[1]) + (
                    BPSK.s[j] * BPSK.cDynamic[2]) + BPSK.sigma * (
                                   complex(random.gauss(0, 1), random.gauss(0, 1)) / math.sqrt(2)))

            BPSK.delta1.append(pow(abs(
                BPSK.rt[j] - (((1) * BPSK.cDynamic[0]) + (BPSK.s[j + 1] * BPSK.cDynamic[1]) + (
                            BPSK.s[j] * BPSK.cDynamic[2]))),
                2))
            BPSK.delta2.append(pow(abs(BPSK.rt[j] - (
                    ((-1) * BPSK.cDynamic[0]) + (BPSK.s[j + 1] * BPSK.cDynamic[1]) + (BPSK.s[j] * BPSK.cDynamic[2]))),
                                   2))

            if BPSK.delta1[j] < BPSK.delta2[j]:
                BPSK.transmittedSymbols.append(1)
            else:
                BPSK.transmittedSymbols.append(-1)


        for k in range(0, len(BPSK.s)):
            if BPSK.s[k] != BPSK.transmittedSymbols[k]:
                BPSK.symErrorCount += 1

        # x = []
        # y = []
        #
        # # for l1 in range(0, len(BPSK.rt)):
        # #     x.append(BPSK.rt[l1].real)
        # #     y.append(BPSK.rt[l1].imag)
        # #
        # # axs[i].scatter(x, y, marker='.', label="Eb/No=" + str(i), color='k', alpha=0.05)
        # # axs[i].legend(loc="upper right", framealpha=0)


        BPSK.SERn[i] += BPSK.symErrorCount
        BPSK.SERd[i] += BPSK.total
        BPSK.SER[i] = BPSK.SERn[i]/BPSK.SERd[i]


    # plt.show()


# fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
# fig.subplots_adjust(hspace=0.001, wspace=0.001)
# axs = axs.ravel()

print("4QAM")
for m in range(0, 500):
    print(colored(m, "green"))
    QAM4.newDynamic()
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
                (QAM4.s[j + 2] * QAM4.cDynamic[0]) + (QAM4.s[j + 1] * QAM4.cDynamic[1]) + (QAM4.s[j] * QAM4.cDynamic[2]) + (
                        QAM4.sigma * (complex(random.gauss(0, 1), random.gauss(0, 1)) / math.sqrt(2))))

            QAM4.delta1.append(pow(abs(QAM4.rt[j] - (((complex(1 / math.sqrt(2), 1 / math.sqrt(2))) * QAM4.cDynamic[0]) + (
                    QAM4.s[j + 1] * QAM4.cDynamic[1]) + (QAM4.s[j] * QAM4.cDynamic[2]))), 2))
            QAM4.delta2.append(pow(abs(QAM4.rt[j] - (((complex(-1 / math.sqrt(2), 1 / math.sqrt(2))) * QAM4.cDynamic[0]) + (
                    QAM4.s[j + 1] * QAM4.cDynamic[1]) + (QAM4.s[j] * QAM4.cDynamic[2]))), 2))
            QAM4.delta3.append(pow(abs(QAM4.rt[j] - (((complex(-1 / math.sqrt(2), -1 / math.sqrt(2))) * QAM4.cDynamic[0]) + (
                    QAM4.s[j + 1] * QAM4.cDynamic[1]) + (QAM4.s[j] * QAM4.cDynamic[2]))), 2))
            QAM4.delta4.append(pow(abs(QAM4.rt[j] - (((complex(1 / math.sqrt(2), -1 / math.sqrt(2))) * QAM4.cDynamic[0]) + (
                    QAM4.s[j + 1] * QAM4.cDynamic[1]) + (QAM4.s[j] * QAM4.cDynamic[2]))), 2))


            if (QAM4.delta1[j] < QAM4.delta2[j]) and (QAM4.delta1[j] < QAM4.delta3[j]) and (
                    QAM4.delta1[j] < QAM4.delta4[j]):
                QAM4.transmittedSymbols.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
            elif (QAM4.delta2[j] < QAM4.delta1[j]) and (QAM4.delta2[j] < QAM4.delta3[j]) and (
                    QAM4.delta2[j] < QAM4.delta4[j]):
                QAM4.transmittedSymbols.append(complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))
            elif (QAM4.delta3[j] < QAM4.delta1[j]) and (QAM4.delta3[j] < QAM4.delta2[j]) and (
                    QAM4.delta3[j] < QAM4.delta4[j]):
                QAM4.transmittedSymbols.append(complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))
            elif (QAM4.delta4[j] < QAM4.delta1[j]) and (QAM4.delta4[j] < QAM4.delta2[j]) and (
                    QAM4.delta4[j] < QAM4.delta3[j]):
                QAM4.transmittedSymbols.append(complex(1 / math.sqrt(2), -1 / math.sqrt(2)))
            else:
                print("Error 4QAM")

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

        # x = []
        # y = []
        #
        # for l1 in range(0, len(QAM4.rt)):
        #     x.append(QAM4.rt[l1].real)
        #     y.append(QAM4.rt[l1].imag)
        #
        # axs[i].scatter(x, y, marker=".", alpha = 0.01, label="Eb/No="+str(i), color='k')
        # axs[i].legend(loc="upper right", framealpha=0)


        QAM4.BERn[i] += QAM4.bitErrorCount
        QAM4.BERd[i] += QAM4.total
        QAM4.BER[i] = QAM4.BERn[i] / QAM4.BERd[i]


    # plt.show()


# fig, axs = plt.subplots(4, 4, sharex='col', sharey='row')
# fig.subplots_adjust(hspace=0.001, wspace=0.001)
# axs = axs.ravel()
for m in range(0, 500):
    print(colored(m, 'blue'))
    PSK8.newDynamic()
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
            PSK8.rt.append(
                (PSK8.s[j + 2] * PSK8.cDynamic[0]) + (PSK8.s[j + 1] * PSK8.cDynamic[1]) + (PSK8.s[j] * PSK8.cDynamic[2]) + (
                        PSK8.sigma * (complex(random.gauss(0, 1), random.gauss(0, 1)) / math.sqrt(2))))

            PSK8.delta1.append(pow(abs(PSK8.rt[j] - (
                    ((complex(1, 0)) * PSK8.cDynamic[0]) + (PSK8.s[j + 1] * PSK8.cDynamic[1]) + (
                    PSK8.s[j] * PSK8.cDynamic[2]))), 2))
            PSK8.delta2.append(pow(abs(PSK8.rt[j] - (((complex(1 / math.sqrt(2), 1 / math.sqrt(2))) * PSK8.cDynamic[0]) + (
                    PSK8.s[j + 1] * PSK8.cDynamic[1]) + (PSK8.s[j] * PSK8.cDynamic[2]))), 2))
            PSK8.delta3.append(pow(abs(PSK8.rt[j] - (
                    ((complex(0, 1)) * PSK8.cDynamic[0]) + (PSK8.s[j + 1] * PSK8.cDynamic[1]) + (
                    PSK8.s[j] * PSK8.cDynamic[2]))), 2))
            PSK8.delta4.append(pow(abs(PSK8.rt[j] - (((complex(-1 / math.sqrt(2), 1 / math.sqrt(2))) * PSK8.cDynamic[0]) + (
                    PSK8.s[j + 1] * PSK8.cDynamic[1]) + (PSK8.s[j] * PSK8.cDynamic[2]))), 2))
            PSK8.delta5.append(pow(abs(PSK8.rt[j] - (
                    ((complex(-1, 0)) * PSK8.cDynamic[0]) + (PSK8.s[j + 1] * PSK8.cDynamic[1]) + (
                    PSK8.s[j] * PSK8.cDynamic[2]))), 2))
            PSK8.delta6.append(pow(abs(PSK8.rt[j] - (((complex(-1 / math.sqrt(2), -1 / math.sqrt(2))) * PSK8.cDynamic[0]) + (
                    PSK8.s[j + 1] * PSK8.cDynamic[1]) + (PSK8.s[j] * PSK8.cDynamic[2]))), 2))
            PSK8.delta7.append(pow(abs(PSK8.rt[j] - (
                    ((complex(0, -1)) * PSK8.cDynamic[0]) + (PSK8.s[j + 1] * PSK8.cDynamic[1]) + (
                    PSK8.s[j] * PSK8.cDynamic[2]))), 2))
            PSK8.delta8.append(pow(abs(PSK8.rt[j] - (((complex(1 / math.sqrt(2), -1 / math.sqrt(2))) * PSK8.cDynamic[0]) + (
                    PSK8.s[j + 1] * PSK8.cDynamic[1]) + (PSK8.s[j] * PSK8.cDynamic[2]))), 2))

            if (PSK8.delta1[j] < PSK8.delta2[j]) and (PSK8.delta1[j] < PSK8.delta3[j]) and (
                    PSK8.delta1[j] < PSK8.delta4[j]) and (PSK8.delta1[j] < PSK8.delta5[j]) and (
                    PSK8.delta1[j] < PSK8.delta6[j]) and (PSK8.delta1[j] < PSK8.delta7[j]) and (
                    PSK8.delta1[j] < PSK8.delta8[j]):
                PSK8.transmittedSymbols.append(complex(1, 0))
            elif (PSK8.delta2[j] < PSK8.delta1[j]) and (PSK8.delta2[j] < PSK8.delta3[j]) and (
                    PSK8.delta2[j] < PSK8.delta4[j]) and (PSK8.delta2[j] < PSK8.delta5[j]) and (
                    PSK8.delta2[j] < PSK8.delta6[j]) and (PSK8.delta2[j] < PSK8.delta7[j]) and (
                    PSK8.delta2[j] < PSK8.delta8[j]):
                PSK8.transmittedSymbols.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
            elif (PSK8.delta3[j] < PSK8.delta1[j]) and (PSK8.delta3[j] < PSK8.delta2[j]) and (
                    PSK8.delta3[j] < PSK8.delta4[j]) and (PSK8.delta3[j] < PSK8.delta5[j]) and (
                    PSK8.delta3[j] < PSK8.delta6[j]) and (PSK8.delta3[j] < PSK8.delta7[j]) and (
                    PSK8.delta3[j] < PSK8.delta8[j]):
                PSK8.transmittedSymbols.append(complex(0, 1))
            elif (PSK8.delta4[j] < PSK8.delta1[j]) and (PSK8.delta4[j] < PSK8.delta2[j]) and (
                    PSK8.delta4[j] < PSK8.delta3[j]) and (PSK8.delta4[j] < PSK8.delta5[j]) and (
                    PSK8.delta4[j] < PSK8.delta6[j]) and (PSK8.delta4[j] < PSK8.delta7[j]) and (
                    PSK8.delta4[j] < PSK8.delta8[j]):
                PSK8.transmittedSymbols.append(complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))
            elif (PSK8.delta5[j] < PSK8.delta1[j]) and (PSK8.delta5[j] < PSK8.delta2[j]) and (
                    PSK8.delta5[j] < PSK8.delta3[j]) and (PSK8.delta5[j] < PSK8.delta4[j]) and (
                    PSK8.delta5[j] < PSK8.delta6[j]) and (PSK8.delta5[j] < PSK8.delta7[j]) and (
                    PSK8.delta5[j] < PSK8.delta8[j]):
                PSK8.transmittedSymbols.append(complex(-1, 0))
            elif (PSK8.delta6[j] < PSK8.delta1[j]) and (PSK8.delta6[j] < PSK8.delta2[j]) and (
                    PSK8.delta6[j] < PSK8.delta3[j]) and (PSK8.delta6[j] < PSK8.delta4[j]) and (
                    PSK8.delta6[j] < PSK8.delta5[j]) and (PSK8.delta6[j] < PSK8.delta7[j]) and (
                    PSK8.delta6[j] < PSK8.delta8[j]):
                PSK8.transmittedSymbols.append(complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))
            elif (PSK8.delta7[j] < PSK8.delta1[j]) and (PSK8.delta7[j] < PSK8.delta2[j]) and (
                    PSK8.delta7[j] < PSK8.delta3[j]) and (PSK8.delta7[j] < PSK8.delta4[j]) and (
                    PSK8.delta7[j] < PSK8.delta5[j]) and (PSK8.delta7[j] < PSK8.delta6[j]) and (
                    PSK8.delta7[j] < PSK8.delta8[j]):
                PSK8.transmittedSymbols.append(complex(0, -1))
            elif (PSK8.delta8[j] < PSK8.delta1[j]) and (PSK8.delta8[j] < PSK8.delta2[j]) and (
                    PSK8.delta8[j] < PSK8.delta3[j]) and (PSK8.delta8[j] < PSK8.delta4[j]) and (
                    PSK8.delta8[j] < PSK8.delta5[j]) and (PSK8.delta8[j] < PSK8.delta6[j]) and (
                    PSK8.delta8[j] < PSK8.delta7[j]):
                PSK8.transmittedSymbols.append(complex(1 / math.sqrt(2), -1 / math.sqrt(2)))
            else:
                print(colored("ERROR in Delta Check", 'red'))

            if PSK8.s[j] != PSK8.transmittedSymbols[j]:
                PSK8.symErrorCount += 1

        PSK8.transmittedSymbols.pop(0)
        PSK8.transmittedSymbols.pop(0)

        for j in range(0, int(PSK8.total / 3)):
            if PSK8.transmittedSymbols[j] == complex(1, 0):
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(1)
            elif PSK8.transmittedSymbols[j] == complex(1 / math.sqrt(2), 1 / math.sqrt(2)):
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(0)
            elif PSK8.transmittedSymbols[j] == complex(0, 1):
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(0)
            elif PSK8.transmittedSymbols[j] == complex(-1 / math.sqrt(2), 1 / math.sqrt(2)):
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(1)
            elif PSK8.transmittedSymbols[j] == complex(-1, 0):
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(1)
            elif PSK8.transmittedSymbols[j] == complex(-1 / math.sqrt(2), -1 / math.sqrt(2)):
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(0)
            elif PSK8.transmittedSymbols[j] == complex(0, -1):
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(0)
            elif PSK8.transmittedSymbols[j] == complex(1 / math.sqrt(2), -1 / math.sqrt(2)):
                PSK8.transmittedBits.append(1)
                PSK8.transmittedBits.append(0)
                PSK8.transmittedBits.append(1)
            else:
                print(colored("ERROR in Sym->Bits Transform", 'red'))

        for l in range(0, len(PSK8.bits)):
            if PSK8.bits[l] != PSK8.transmittedBits[l]:
                PSK8.bitErrorCount += 1

        # x = []
        # y = []
        #
        # for l1 in range(0, len(PSK8.rt)):
        #     x.append(PSK8.rt[l1].real)
        #     y.append(PSK8.rt[l1].imag)
        #
        # axs[i].scatter(x, y, marker=".", alpha=0.01, label="Eb/No="+str(i), color='k')
        # axs[i].legend(loc="upper right", framealpha=0)

        PSK8.BERn[i] += PSK8.bitErrorCount
        PSK8.BERd[i] += PSK8.total
        PSK8.BER[i] = PSK8.BERn[i] / PSK8.BERd[i]

    # plt.show()


x = []
for i in range(0, 16):
    x.append(i)
plt.semilogy(x, BPSK.SER, 'r-', label="BPSK BER")
# plt.semilogy(x, QAM4.SER, 'k-', label="4QAM SER")
plt.semilogy(x, QAM4.BER, 'k-', label="4QAM BER")
# plt.semilogy(x, PSK8.SER, 'b-', label="8PSK SER")
plt.semilogy(x, PSK8.BER, 'b-', label="8PSK BER")


plt.xlabel("Eb/No")
plt.ylabel("Bit Error Rate (BER) for Dynamic CIR")
plt.legend()
plt.show()