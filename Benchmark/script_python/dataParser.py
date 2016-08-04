POSITION_PREFIX     = "pos_"
POSITION_SEPARATOR  = "\t"
TIMESTAMP_PREFIX    = "data_"
TIMESTAMP_SEPARATOR = ";"
FILES_RELATIVE_PATH = "./"
OUTPUT_FILE         = "output.txt"


TILE_SIZE   =  500  # Même unitée que celle utilisée dans les fichiers de positionnement. A priori mm.
TABLE_X_MAX =  1500
TABLE_X_MIN = -1500
TABLE_Y_MAX =  2000
TABLE_Y_MIN =  0

# Les dimmensions de la table doivent être un multiple de TILE_SIZE
TABLE_X_MAX += TABLE_X_MAX % TILE_SIZE
TABLE_X_MIN += TABLE_X_MIN % TILE_SIZE
TABLE_Y_MAX += TABLE_Y_MAX % TILE_SIZE
TABLE_Y_MIN += TABLE_Y_MIN % TILE_SIZE


# Il faut faire correspondre cela au format des fichiers d'entrée (c'est l'ordre des données sur chaque ligne)
_X      = 0
_Y      = 1
CANAL_1 = 0
CANAL_2 = 1
INT     = 2


from os import walk
from statistics import median
import json

dirFileNames = []
for (dirPath, dirNames, fileNames) in walk(FILES_RELATIVE_PATH):
    dirFileNames.extend(fileNames)
    break

positionFiles = []
timestampFiles = []
for name in dirFileNames:
    if name.find(POSITION_PREFIX) == 0:
        positionFiles.append(name)
    elif name.find(TIMESTAMP_PREFIX) == 0:
        timestampFiles.append(name)

pairedFiles = []  # [(positionFilename, timestampFilename), ... ]
for posName in positionFiles:
    identifier = posName[len(POSITION_PREFIX):]
    for timeName in timestampFiles:
        if timeName[len(TIMESTAMP_PREFIX):] == identifier:
            pairedFiles.append((posName, timeName))

print(len(pairedFiles), " pair(s) of files found")

rawData = [] # [((x,y),(K2,K3)), ... ]
for pair in pairedFiles:
    try:
        posFile = open(FILES_RELATIVE_PATH + pair[0], 'r')
        timeFile = open(FILES_RELATIVE_PATH + pair[1], 'r')
        endReached = False
        while not endReached:
            positionStr = posFile.readline()
            timestampStr = timeFile.readline()
            if len(positionStr) == 0 or len(timestampStr) == 0:
                endReached = True
            else:
                posList = positionStr.split(POSITION_SEPARATOR)
                timeList = timestampStr.split(TIMESTAMP_SEPARATOR)
                if len(posList) == 2 and len(timeList) == 3:
                    x = float(posList[_X])
                    y = float(posList[_Y])
                    k2 = float(timeList[INT]) - float(timeList[CANAL_1])
                    k3 = float(timeList[CANAL_2]) - float(timeList[CANAL_1])
                    if TABLE_X_MIN <= x <= TABLE_X_MAX and TABLE_Y_MIN <= y <= TABLE_Y_MAX:
                        rawData.append(((x,y),(k2,k3)))
                    else:
                        print("Position hors table !")
        posFile.close()
        timeFile.close()
    except OSError:
        print("Failed to open files: " + FILES_RELATIVE_PATH + pair[0] + " and " + FILES_RELATIVE_PATH + pair[1])


nbL = int((TABLE_Y_MAX - TABLE_Y_MIN) / TILE_SIZE)
nbC = int((TABLE_X_MAX - TABLE_X_MIN) / TILE_SIZE)

regroupedData = []  # [ [ [(K2,K3), ... ], ... ], ... ]
for line in range(nbL):
    regroupedData.append([])
    for column in range(nbC):
        regroupedData[line].append([])

for point in rawData:
    column = int((point[0][0] - TABLE_X_MIN) / TILE_SIZE)
    line = int((point[0][1] - TABLE_Y_MIN) / TILE_SIZE)
    regroupedData[line][column].append(point[1])

finalData = []  # [ [K2, K3, x, y], ... ]
for line in range(len(regroupedData)):
    for column in range(len(regroupedData[line])):
        k2List = [couple[0] for couple in regroupedData[line][column]]
        k3List = [couple[1] for couple in regroupedData[line][column]]
        if len(k2List) == 0:
            k2 = None
        else:
            k2 = median(k2List)
        if len(k3List) == 0:
            k3 = None
        else:
            k3 = median(k3List)
        x = TABLE_X_MIN + column*TILE_SIZE + TILE_SIZE/2
        y = TABLE_Y_MIN + line*TILE_SIZE + TILE_SIZE/2
        finalData.append([k2, k3, x, y])


try:
    output = open(OUTPUT_FILE, 'w')
    json.dump(finalData, output)
    output.close()
    print("Output written into: " + OUTPUT_FILE)
except OSError:
    print("Failed to write the output file: " + OUTPUT_FILE)
