# Manufacturing Entropy - Code for the article
# Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Yamila Mariel Omar
# Date of original code: 15th November 2016
# Date of code last modification: 15th April 2020

import re

# Read the file
fileName = 'data/train_date.csv'
fileHandle = open(fileName)

aux = 0
myDict = {}
myEdges = {}
for row in fileHandle:

    if (aux == 0):
        colNames = row.strip().split(',')
        del colNames[0]
        aux = 1
        continue

    row = row.strip().split(',')
    indexN = int(row.pop(0))    # 'Id'

    # Remove Null
    notNull = ['' == i for i in row]
    myCols = [i for (i, v) in zip(colNames, notNull) if not v]
    row = filter(None, row)

    # Make elements floats
    row = [float(i) for i in row]

    # Change to mean values for each visited station
    vStat = list(set(re.findall('L.(_S.+?_)D', ' '.join(myCols))))
    timeStamp = []
    for s in vStat:
        c = [s in i for i in myCols]
        sensorData = [v for (i,v) in zip(c,row) if i]
        sensorData = sum(sensorData) / float(len(sensorData))
        timeStamp.append(sensorData)

    vStat_ord = [s for (t,s) in sorted(zip(timeStamp, vStat))]
    vStat_ord = [re.findall('_S([0-9]+)_', i)[0] for i in vStat_ord]
    vStat_ord = [int(i) for i in vStat_ord]
    vStat_ord = tuple(vStat_ord)
    if len(vStat_ord)==0: continue
    myDict[vStat_ord] = myDict.get(vStat_ord, 0) + 1
    edges = [('i',vStat_ord[0])] + [(i,j) for (i,j) in zip(vStat_ord, vStat_ord[1:])] + [(vStat_ord[len(vStat_ord)-1], 'f')]
    for e in edges:
        myEdges[e] = myEdges.get(e, 0) + 1

fileHandle.close()

# del re, fileName, fileHandle, aux, row, colNames, indexN, notNull, myCols, i, vStat, timeStamp
# del s, c, sensorData, vStat_ord, t, j, e, v, edges

# ===========================================================
# Saving the data for all paths
# Data is saved as stations + count (count is the last item)
f = open('data/manufacturing_paths.txt', 'w')

for k,v in myDict.items():
    line = ' '.join(str(x) for x in k)
    line = line + ' ' + str(v)
    f.write(line + '\n')

f.close()

# Saving the data for all edges
# Data is saved as stations + count (count is the last item)
f = open('data/manufacturing_edges.txt', 'w')

for k,v in myEdges.items():
    line = ' '.join(str(x) for x in k)
    line = line + ' ' + str(v)
    f.write(line + '\n')

f.close()

del f, k, v, line

# ===========================================================
