import question_1
import question_2
import math
import matplotlib.pyplot as plt
import cmath
from numpy import linspace, asarray
import time

uniform = question_1.PRNG()

bpskDict ={
    "0": [0],
    "1": [1]
}

qam4Dict = {
    "00": [0, 0],
    "01": [0, 1],
    "10": [1, 0],
    "11": [1, 1]
}

psk8Dict = {
    "000": [0, 0, 0],
    "001": [0, 0, 1],
    "010": [0, 1, 0],
    "011": [0, 1, 1],
    "100": [1, 0, 0],
    "101": [1, 0, 1],
    "110": [1, 1, 0],
    "111": [1, 1, 1]
}

dictionary = {
    "0000": [0, 0, 0, 0],
    "0001": [0, 0, 0, 1],
    "0010": [0, 0, 1, 0],
    "0011": [0, 0, 1, 1],
    "0100": [0, 1, 0, 0],
    "0101": [0, 1, 0, 1],
    "0110": [0, 1, 1, 0],
    "0111": [0, 1, 1, 1],
    "1000": [1, 0, 0, 0],
    "1001": [1, 0, 0, 1],
    "1010": [1, 0, 1, 0],
    "1011": [1, 0, 1, 1],
    "1100": [1, 1, 0, 0],
    "1101": [1, 1, 0, 1],
    "1110": [1, 1, 1, 0],
    "1111": [1, 1, 1, 1]
}


class Modulation:
    def __init__(self, bits, numM):
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
        temp = uniform.randomUniform()
        if temp > 0.5:
            self.bits.append(1)
        else:
            self.bits.append(0)


norm = question_2.GRNG()

# Class Instances (total number of bits, and the M value)
BPSK = Modulation(10000, 2)
QAM4 = Modulation(10000, 4)
PSK8 = Modulation(10002, 8)
QAM16 = Modulation(10000, 16)


# new comment
def mapBPSK():
    # Converts bits to symbols
    for i in range(0, BPSK.total):
        BPSK.binary()
        length = len(BPSK.bits)
        if BPSK.bits[length - 1] == 1:
            BPSK.symbols.append(1)
        else:
            BPSK.symbols.append(-1)

    for i in range(-4, 13):
        start_time = time.time()
        print(i)

        BPSK.bitErrorCount = 0
        BPSK.symErrorCount = 0
        BPSK.transmittedBits = []
        BPSK.transmittedSymbols = []
        BPSK.rk = []

        for j in range(0, BPSK.total):
            # Adding AWGN
            BPSK.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log(BPSK.M, 2)))
            BPSK.rk.append(BPSK.symbols[j] + BPSK.sigma * norm.randomNormal())

            # Decoding Received Bits
            if BPSK.rk[j] >= 0:
                BPSK.transmittedSymbols.append(1)
            else:
                BPSK.transmittedSymbols.append(-1)

            if BPSK.transmittedSymbols[j] == 1:
                BPSK.transmittedBits.append(1)
            else:
                BPSK.transmittedBits.append(0)

            if BPSK.transmittedSymbols[j] != BPSK.symbols[j]:
                BPSK.symErrorCount += 1

            if BPSK.transmittedBits[j] != BPSK.bits[j]:
                BPSK.bitErrorCount += 1

        BPSK.SER.append(BPSK.symErrorCount / BPSK.total)
        BPSK.BER.append(BPSK.bitErrorCount / BPSK.total)

        # print(time.time() - start_time)

        # Scatter Plot
        # y = [i] * BPSK.total
        # plt.scatter(BPSK.rk, y, alpha=0.05)

    x = []
    for i in range(-4, 13):
        x.append(i)
    plt.semilogy(x, BPSK.SER, 'y--', label="BPSK BER")
    plt.semilogy(x, BPSK.BER, 'y-', label="BPSK SER")


def map4QAM():
    # Converting bits to symbols
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

    # ScatterPlots
    # fig, axs = plt.subplots(4, 5, sharex='col', sharey='row')
    # fig.subplots_adjust(hspace=0.001, wspace=0.001)
    # axs = axs.ravel()

    for i in range(-4, 13):
        print(i)
        QAM4.symErrorCount = 0
        QAM4.bitErrorCount = 0
        QAM4.transmittedBits = []
        QAM4.transmittedSymbols = []
        QAM4.rk = []

        for j in range(int(QAM4.total / 2)):
            # Adding Gaussian Noise
            QAM4.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log(QAM4.M, 2)))
            QAM4.rk.append(QAM4.symbols[j] + QAM4.sigma * complex(norm.randomNormal(), norm.randomNormal()))

            # Calculating the Euclidean Distance to each point
            value = abs(QAM4.rk[j] - complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
            tempSymbol = "00"

            # Checking 01
            tempValue = abs(QAM4.rk[j] - complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))
            if tempValue < value:
                value = tempValue
                tempSymbol = "01"

            # Checking 11
            tempValue = abs(QAM4.rk[j] - complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))
            if tempValue < value:
                value = tempValue
                tempSymbol = "11"

            # Checking 10
            tempValue = abs(QAM4.rk[j] - complex(1 / math.sqrt(2), -1 / math.sqrt(2)))
            if tempValue < value:
                value = tempValue
                tempSymbol = "10"

            QAM4.transmittedBits.extend(qam4Dict.get(tempSymbol))

            x = []
            y = []

        # Subplots
        # for l in range(0, len(QAM4.rk)):
        #     x.append(QAM4.rk[l].real)
        #     y.append(QAM4.rk[l].imag)
        #
        # axs[i+4].scatter(x, y, marker=".", alpha = 0.05, label=str(i), color='k')
        # axs[i+4].legend( loc="upper right", framealpha=0)

        # Calculating bit error
        for j in range(QAM4.total):
            if QAM4.bits[j] != QAM4.transmittedBits[j]:
                QAM4.bitErrorCount += 1

            temp1 = ["X"] * 2
            temp2 = ["X"] * 2

            temp1[j % 2] = QAM4.bits[j]
            temp2[j % 2] = QAM4.transmittedBits[j]
            if (j % 2 + 1) == 2:
                if temp1 != temp2:
                    QAM4.symErrorCount += 1

        QAM4.SER.append(QAM4.symErrorCount / (QAM4.total / 2))
        QAM4.BER.append(QAM4.bitErrorCount / QAM4.total)

    # Plotting the SER and BER for 4QAM
    x = []
    for i in range(-4, 13):
        x.append(i)
    plt.semilogy(x, QAM4.BER, 'r--', label="4QAM BER")
    plt.semilogy(x, QAM4.SER, 'r-', label="4QAM SER")


def map8PSK():
    # Converting bits to symbols
    tri = [0] * 3
    for i in range(PSK8.total):
        PSK8.binary()
        tri[i % 3] = PSK8.bits[i]
        if (i % 3 + 1) == 3:
            if tri[0] == 0 and tri[1] == 0 and tri[2] == 0:
                PSK8.symbols.append(complex(1, 0))

            elif tri[0] == 0 and tri[1] == 0 and tri[2] == 1:
                PSK8.symbols.append(complex(1 / math.sqrt(2), 1 / math.sqrt(2)))

            elif tri[0] == 0 and tri[1] == 1 and tri[2] == 1:
                PSK8.symbols.append(complex(0, 1))

            elif tri[0] == 0 and tri[1] == 1 and tri[2] == 0:
                PSK8.symbols.append(complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))

            elif tri[0] == 1 and tri[1] == 1 and tri[2] == 0:
                PSK8.symbols.append(complex(-1, 0))

            elif tri[0] == 1 and tri[1] == 1 and tri[2] == 1:
                PSK8.symbols.append(complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))

            elif tri[0] == 1 and tri[1] == 0 and tri[2] == 1:
                PSK8.symbols.append(complex(0, -1))

            elif tri[0] == 1 and tri[1] == 0 and tri[2] == 0:
                PSK8.symbols.append(complex(1 / math.sqrt(2), -1 / math.sqrt(2)))

    # Subplots
    # fig, axs = plt.subplots(4, 5, sharex='col', sharey='row')
    # fig.subplots_adjust(hspace=0.001, wspace=0.001)
    # axs = axs.ravel()

    for i in range(-4, 13):
        print(i)
        for j in range(int(PSK8.total / 3)):
            # Adding Gaussian Noise
            PSK8.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log2(PSK8.M)))
            PSK8.rk.append(PSK8.symbols[j] + PSK8.sigma * complex(norm.randomNormal(), norm.randomNormal()))

            # Calculating the Euclidean Distance to each point
            value = abs(PSK8.rk[j] - complex(1, 0))
            tempSymbol = "000"

            # Checking 001
            tempValue = abs(PSK8.rk[j] - complex(1 / math.sqrt(2), 1 / math.sqrt(2)))
            if tempValue < value:
                value = tempValue
                tempSymbol = "001"

            # Checking 011
            tempValue = abs(PSK8.rk[j] - complex(0, 1))
            if tempValue < value:
                value = tempValue
                tempSymbol = "011"

            # Checking 010
            tempValue = abs(PSK8.rk[j] - complex(-1 / math.sqrt(2), 1 / math.sqrt(2)))
            if tempValue < value:
                value = tempValue
                tempSymbol = "010"

            # Checking 110
            tempValue = abs(PSK8.rk[j] - complex(-1, 0))
            if tempValue < value:
                value = tempValue
                tempSymbol = "110"

            # Checking 111
            tempValue = abs(PSK8.rk[j] - complex(-1 / math.sqrt(2), -1 / math.sqrt(2)))
            if tempValue < value:
                value = tempValue
                tempSymbol = "111"

            # Checking 101
            tempValue = abs(PSK8.rk[j] - complex(0, -1))
            if tempValue < value:
                value = tempValue
                tempSymbol = "101"

            # Checking 100
            tempValue = abs(PSK8.rk[j] - complex(1 / math.sqrt(2), -1 / math.sqrt(2)))
            if tempValue < value:
                value = tempValue
                tempSymbol = "100"

            PSK8.transmittedBits.extend(psk8Dict.get(tempSymbol))

            x = []
            y = []

        # Subplots
        # for l in range(0, len(PSK8.rk)):
        #     x.append(PSK8.rk[l].real)
        #     y.append(PSK8.rk[l].imag)
        #
        # axs[i+4].scatter(x, y, marker=".", alpha = 0.05, label=str(i), color='k')
        # axs[i+4].legend(loc="upper right", framealpha=0)

        # Calculating bit error
        for j in range(PSK8.total):
            if PSK8.bits[j] != PSK8.transmittedBits[j]:
                PSK8.bitErrorCount += 1

            temp1 = ["X"] * 3
            temp2 = ["X"] * 3

            temp1[j % 3] = PSK8.bits[j]
            temp2[j % 3] = PSK8.transmittedBits[j]
            if (j % 3 + 1) == 3:
                if temp1 != temp2:
                    PSK8.symErrorCount += 1

        PSK8.SER.append(PSK8.symErrorCount / (PSK8.total / 3))

        PSK8.BER.append(PSK8.bitErrorCount / PSK8.total)

        PSK8.symErrorCount = 0
        PSK8.bitErrorCount = 0
        PSK8.transmittedBits = []
        PSK8.transmittedSymbols = []
        PSK8.rk = []

    # Plotting the SER and BER for 8PSK
    x = []
    for i in range(-4, 13):
        x.append(i)
    plt.semilogy(x, PSK8.BER, 'm--', label="8PSK BER")
    plt.semilogy(x, PSK8.SER, 'm-', label="8PSK SER")


def map16QAM():
    # Convert to Symbols
    quad = [0] * 4
    for i in range(0, QAM16.total):
        QAM16.binary()
        quad[i % 4] = QAM16.bits[i]
        if (i % 4 + 1) == 4:
            if quad[0] == 0 and quad[1] == 0 and quad[2] == 0 and quad[3] == 0:
                QAM16.symbols.append(complex(-1 / (math.sqrt(2)), 1 / (math.sqrt(2))))
            elif quad[0] == 0 and quad[1] == 0 and quad[2] == 0 and quad[3] == 1:
                QAM16.symbols.append(complex(-1 / (math.sqrt(2)), math.sqrt(2) / 6))
            elif quad[0] == 0 and quad[1] == 0 and quad[2] == 1 and quad[3] == 0:
                QAM16.symbols.append(complex(-1 / (math.sqrt(2)), -1 / (math.sqrt(2))))
            elif quad[0] == 0 and quad[1] == 0 and quad[2] == 1 and quad[3] == 1:
                QAM16.symbols.append(complex(-1 / (math.sqrt(2)), -math.sqrt(2) / 6))
            elif quad[0] == 0 and quad[1] == 1 and quad[2] == 0 and quad[3] == 0:
                QAM16.symbols.append(complex(-math.sqrt(2) / 6, 1 / (math.sqrt(2))))
            elif quad[0] == 0 and quad[1] == 1 and quad[2] == 0 and quad[3] == 1:
                QAM16.symbols.append(complex(-math.sqrt(2) / 6, math.sqrt(2) / 6))
            elif quad[0] == 0 and quad[1] == 1 and quad[2] == 1 and quad[3] == 0:
                QAM16.symbols.append(complex(-math.sqrt(2) / 6, -1 / (math.sqrt(2))))
            elif quad[0] == 0 and quad[1] == 1 and quad[2] == 1 and quad[3] == 1:
                QAM16.symbols.append(complex(-math.sqrt(2) / 6, -math.sqrt(2) / 6))
            elif quad[0] == 1 and quad[1] == 0 and quad[2] == 0 and quad[3] == 0:
                QAM16.symbols.append(complex(1 / (math.sqrt(2)), 1 / (math.sqrt(2))))
            elif quad[0] == 1 and quad[1] == 0 and quad[2] == 0 and quad[3] == 1:
                QAM16.symbols.append(complex(1 / (math.sqrt(2)), math.sqrt(2) / 6))
            elif quad[0] == 1 and quad[1] == 0 and quad[2] == 1 and quad[3] == 0:
                QAM16.symbols.append(complex(1 / (math.sqrt(2)), -1 / (math.sqrt(2))))
            elif quad[0] == 1 and quad[1] == 0 and quad[2] == 1 and quad[3] == 1:
                QAM16.symbols.append(complex(1 / (math.sqrt(2)), -math.sqrt(2) / 6))
            elif quad[0] == 1 and quad[1] == 1 and quad[2] == 0 and quad[3] == 0:
                QAM16.symbols.append(complex(math.sqrt(2) / 6, 1 / (math.sqrt(2))))
            elif quad[0] == 1 and quad[1] == 1 and quad[2] == 0 and quad[3] == 1:
                QAM16.symbols.append(complex(math.sqrt(2) / 6, math.sqrt(2) / 6))
            elif quad[0] == 1 and quad[1] == 1 and quad[2] == 1 and quad[3] == 0:
                QAM16.symbols.append(complex(math.sqrt(2) / 6, -1 / (math.sqrt(2))))
            elif quad[0] == 1 and quad[1] == 1 and quad[2] == 1 and quad[3] == 1:
                QAM16.symbols.append(complex(math.sqrt(2) / 6, -math.sqrt(2) / 6))

    # Subplots
    # fig, axs = plt.subplots(4, 5, sharex='col', sharey='row')
    # fig.subplots_adjust(hspace=0.001, wspace=0.001)
    # axs = axs.ravel()

    for i in range(-4, 13):
        print(i)
        # print(i)
        for j in range(0, int(QAM16.total / 4)):
            # Adding AWGN
            QAM16.sigma = 1 / (math.sqrt(10 ** (i / 10) * 2 * math.log(QAM16.M, 2)))
            QAM16.rk.append(QAM16.symbols[j] + QAM16.sigma * complex(norm.randomNormal(), norm.randomNormal()))

            value = abs(QAM16.rk[j] - (complex(-1 / (math.sqrt(2)), 1 / (math.sqrt(2)))))
            tempSym = "0000"
            tempValue = abs(QAM16.rk[j] - (complex(-1 / (math.sqrt(2)), math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "0001"

            tempValue = abs(QAM16.rk[j] - (complex(-1 / (math.sqrt(2)), -1 / (math.sqrt(2)))))
            if tempValue < value:
                value = tempValue
                tempSym = "0010"

            tempValue = abs(QAM16.rk[j] - (complex(-1 / (math.sqrt(2)), -math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "0011"

            tempValue = abs(QAM16.rk[j] - (complex(-math.sqrt(2) / 6, 1 / (math.sqrt(2)))))
            if tempValue < value:
                value = tempValue
                tempSym = "0100"
            tempValue = abs(QAM16.rk[j] - (complex(-math.sqrt(2) / 6, math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "0101"
            tempValue = abs(QAM16.rk[j] - (complex(-math.sqrt(2) / 6, -1 / (math.sqrt(2)))))
            if tempValue < value:
                value = tempValue
                tempSym = "0110"
            tempValue = abs(QAM16.rk[j] - (complex(-math.sqrt(2) / 6, -math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "0111"
            tempValue = abs(QAM16.rk[j] - (complex(1 / (math.sqrt(2)), 1 / (math.sqrt(2)))))
            if tempValue < value:
                value = tempValue
                tempSym = "1000"
            tempValue = abs(QAM16.rk[j] - (complex(1 / (math.sqrt(2)), math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "1001"
            tempValue = abs(QAM16.rk[j] - (complex(1 / (math.sqrt(2)), -1 / (math.sqrt(2)))))
            if tempValue < value:
                value = tempValue
                tempSym = "1010"
            tempValue = abs(QAM16.rk[j] - (complex(1 / (math.sqrt(2)), -math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "1011"
            tempValue = abs(QAM16.rk[j] - (complex(math.sqrt(2) / 6, 1 / (math.sqrt(2)))))
            if tempValue < value:
                value = tempValue
                tempSym = "1100"
            tempValue = abs(QAM16.rk[j] - (complex(math.sqrt(2) / 6, math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "1101"
            tempValue = abs(QAM16.rk[j] - (complex(math.sqrt(2) / 6, -1 / (math.sqrt(2)))))
            if tempValue < value:
                value = tempValue
                tempSym = "1110"
            tempValue = abs(QAM16.rk[j] - (complex(math.sqrt(2) / 6, -math.sqrt(2) / 6)))
            if tempValue < value:
                value = tempValue
                tempSym = "1111"

            QAM16.transmittedBits.extend(dictionary.get(tempSym))

            x = []
            y = []

        # Subplots
        # for l in range(0, len(QAM16.rk)):
        #     x.append(QAM16.rk[l].real)
        #     y.append(QAM16.rk[l].imag)
        # axs[i + 4].scatter(x, y, marker=".", alpha=0.05, label=str(i), color='k')
        # axs[i + 4].legend(loc="upper right", framealpha=0)

        for j in range(0, QAM16.total):
            if QAM16.bits[j] != QAM16.transmittedBits[j]:
                QAM16.bitErrorCount += 1

            tempArray1 = ["X"] * 4
            tempArray2 = ["X"] * 4

            tempArray1[j % 4] = QAM16.bits[j]
            tempArray2[j % 4] = QAM16.transmittedBits[j]
            if (j % 4 + 1) == 4:
                if tempArray1 != tempArray2:
                    QAM16.symErrorCount += 1

        QAM16.SER.append(QAM16.symErrorCount / (QAM16.total / 4))

        QAM16.BER.append(QAM16.bitErrorCount / QAM16.total)

        QAM16.symErrorCount = 0
        QAM16.bitErrorCount = 0
        QAM16.transmittedBits = []
        QAM16.transmittedSymbols = []
        QAM16.rk = []

    x = []
    for i in range(-4, 13):
        x.append(i)
    plt.semilogy(x, QAM16.BER, 'g--', label="16QAM BER")
    plt.semilogy(x, QAM16.SER, 'g-', label="16QAM SER")


# Main of the Program
# Increase number of bits in class instances above to create better line
# Uncomment the function in which you wish to call
# ----------
# mapBPSK()
# print("Done BPSK")
# map4QAM()
# print("Done 4QAM")
# map8PSK()
# print("Done 8PSK")
# map16QAM()
# # Plotting the Graphs using semilogy
# plt.xlabel("Eb/No (dB)")
# plt.ylabel("BER and SER")
# plt.legend()
# plt.show()
# ----------


