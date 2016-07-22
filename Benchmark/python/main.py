from math import sqrt
import matplotlib.pyplot as plt

def main():
    filename = "Test acquisition vanilla-chocolate"
    file = open("../" + filename + ".txt")
    data = readDataFile_orderedFormat(file)
    file.close()

    # data = adjustRawData(data, 6500)

    L = 3000
    l = 2000
    speedOfSound = 0.34  # in mm/µs

    positionsEq1_x = []
    positionsEq1_y = []
    positionsEq2_x = []
    positionsEq2_y = []
    k2_list = []
    k3_list = []

    for i in range(len(data[0])):
        k2_t = data[2][i] - data[0][i]
        k3_t = data[1][i] - data[0][i]
        k2 = k2_t * speedOfSound
        k3 = k3_t * speedOfSound
        k2_list.append(k2)
        k3_list.append(k3)
        position = getXY(k2, k3, L, l)
        aberrant = False
        for value in position:
            if value < -1500 or value > 2000:
                aberrant = True
        if not aberrant:
            positionsEq1_x.append(position[0])
            positionsEq1_y.append(position[1])
            positionsEq2_x.append(position[2])
            positionsEq2_y.append(position[3])
        else:
            print("Valeur aberrante")

    plt.figure()
    plt.plot(positionsEq1_x, positionsEq1_y, 'ro')
    plt.plot(positionsEq2_x, positionsEq2_y, 'go')
    plt.savefig("output_" + filename + ".png")
    plt.close()
    plt.figure()
    plt.plot(k2_list)
    plt.savefig("k2_" + filename + ".png")
    plt.close()
    plt.figure()
    plt.plot(k3_list)
    plt.savefig("k3_" + filename + ".png")
    plt.close()


def readDataFile_rawFormat(file):
    data = [[], [], []]
    for line in file:
        splitLine = line.split(";")
        beaconIndex = int(splitLine[0])
        timestamp = int(splitLine[1])
        data[beaconIndex].append(timestamp)
    return data


def readDataFile_orderedFormat(file):
    data = [[], [], []]
    lineCount = 0
    for line in file:
        try:
            splitLine = line.split(";")
            data[0].append(int(splitLine[0]))
            data[1].append(int(splitLine[1]))
            data[2].append(int(splitLine[2]))
        except ValueError:
            print("Skip line nb" + str(lineCount))
        lineCount += 1
    return data


def adjustRawData(data, maxTimeDifference):
    newData = data
    i = 0
    while i < min(len(newData[0]), len(newData[1]), len(newData[2])):
        toDelete = []
        for beacon in range(3):
            for otherBeacon in range(3):
                if otherBeacon != beacon:
                    if newData[otherBeacon][i] - newData[beacon][i] > maxTimeDifference:
                        toDelete.append(beacon)

        if len(toDelete) == 0:
            i += 1
        else:
            for item in toDelete:
                print("pop b" + str(item) + " #" + str(i))
                newData[item].pop(i)

    for beaconData in newData:
        while len(beaconData) > i:
            print("POP!")
            beaconData.pop()

    return newData


# POSITIONING CALCULATION

def getXY(k2, k3, L, l):
    cte = -(-2*k2+k3)**2*l**2*(k3**2-l**2)*(4*k2**2-l**2-4*L**2)*(4*k2**2-8*k2*k3+4*k3**2-l**2-4*L**2)
    if cte >= 0:
        sq = sqrt(cte)
    else:
        print("cte= " + str(cte) + "  k2= " + str(k2) + "  k3= " + str(k3))
        return [0, 0, 0, 0]

    ax = -8*k2**2*k3**2*L+8*k2*k3**3*L-4*k3**2*l**2*L+2*l**4*L
    bx = sq
    cx = 4*(4*k2**2*l**2-4*k2*k3*l**2+k3**2*l**2+4*k3**2*L**2-4*l**2*L**2)

    ay = 16*k2**4*k3*l**2-32*k2**3*k3**2*l**2+20*k2**2*k3**3*l**2-4*k2*k3**4*l**2+16*k2**3*l**4-20*k2**2*k3*l**4+8*k2*k3**2*l**4-k3**3*l**4-16*k2**2*k3*l**2*L**2+32*k2*k3**2*l**2*L**2-12*k3**3*l**2*L**2-16*k2*l**4*L**2+8*k3*l**4*L**2
    by = 2*k3*L*sq
    cy = 4*(2*k2-k3)*l*(4*k2**2*l**2-4*k2*k3*l**2+k3**2*l**2+4*k3**2*L**2-4*l**2*L**2)

    X1 = (ax + bx) / cx
    Y1 = (ay + by) / cy
    X2 = (ax - bx) / cx
    Y2 = (ay - by) / cy

    return [X1, Y1, X2, Y2]


main()









