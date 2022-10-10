import csv
from fileutils import writeResults
from partsutils import Part, getPart, getParent, getDuplicatePart, toPartsList

def calculateQuantityByItemNumber(partsList):
    results = []
    for part in partsList:
        print(part.itemQuantityToBuildParent)
        accumulatingQuantity = int(part.itemQuantityToBuildParent)
        parentPart = getParent(part.itemNumber, partsList)
        while(parentPart is not None):
            accumulatingQuantity = accumulatingQuantity * int(parentPart.itemQuantityToBuildParent)
            parentPart = getParent(parentPart.itemNumber, partsList)
        part.itemQuantityToBuildPod = accumulatingQuantity
    return partsList


def calculateQuantityByPartNumber(quantityByItemNumber):
    partsDict = {}
    partsResults = []
    for part in quantityByItemNumber:
        springPartNumber = part.springPartNumber
        totalQuantity = part.itemQuantityToBuildPod
        if springPartNumber is not None:
            if springPartNumber not in partsDict:
                partsDict[springPartNumber] = totalQuantity
            else:
                partsDict[springPartNumber] = partsDict[springPartNumber] + totalQuantity
    for key, value in partsDict.items():
        row = [key, value]
        partsResults.append(row)
    partsResults.sort()
    return partsResults

def writeQuantityByItemNumber(partsList):
    path = ('./results/byItemNumber.csv')
    header = ['item number', 'sprint part number', 'item quantity to build parent', 'item quantity for whole pod']
    rows = []
    for part in partsList:
        row = [
            part.itemNumber
            , part.springPartNumber
            , part.itemQuantityToBuildParent
            , part.itemQuantityToBuildPod]
        rows.append(row)
    writeResults(path, header, rows)

def writeQuantityByPartNumber(quantityByPartNumber):
    path = ('./results/byPart.csv')
    header = ["sprint part number", "part quantity for whole pod"]
    writeResults(path, header, quantityByPartNumber)


with open('data.csv') as f:
    reader = csv.reader(f)
    partsListRaw = list(reader)
    f.close()

partsListRaw.pop(0)
partsList = toPartsList(partsListRaw)

duplicatePart = getDuplicatePart(partsList)
if not (duplicatePart):
    partsList = calculateQuantityByItemNumber(partsList)
    writeQuantityByItemNumber(partsList)
    quantityByPartNumber = calculateQuantityByPartNumber(partsList)
    writeQuantityByPartNumber(quantityByPartNumber)

else:
    print("Duplicate found: " + duplicatePart[0])
