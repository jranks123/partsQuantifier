import csv


def getPart(partName, partsList):
    for part in partsList:
        if (part[0] == partName):
            return part

def getParent(part, partsList):
    if("." not in part):
        return None
    partParts = part.split(".")
    partParts.pop()
    parent = ".".join(partParts)
    return getPart(parent, partsList)

def getDuplicatePart(partsList):
    partsDict = {}
    for part in partsList:
        if part[0] not in partsDict:
            partsDict[part[0]] = 1
        else:
            return part


def runQuant():
    f = open('./results/byItemNumber.csv', 'w')
    writer = csv.writer(f)
    header = ['item number', 'sprint part number', 'quantity', 'total quantity']
    writer.writerow(header)

    results = []

    for part in partsList:
        accumulatingQuantity = int(part[6])
        parentPart = getParent(part[0], partsList)
        while(parentPart is not None):
            accumulatingQuantity = accumulatingQuantity * int(parentPart[6])
            parentPart = getParent(parentPart[0], partsList)
        row = [part[0], part[1], part[6], accumulatingQuantity]
        results.append(row)
        writer.writerow(row)
    f.close()

    f = open('./results/byPart.csv', 'w')
    writer = csv.writer(f)
    header = ["sprint part number", "total quantity"]
    writer.writerow(header)
    partsDict = {}
    partsResults = []
    for part in results:
        if part[1] is not None:
            if part[1] not in partsDict:
                partsDict[part[1]] = part[3]
            else:
                partsDict[part[1]] = partsDict[part[1]] + part[3]
    for key, value in partsDict.items():
        row = [key, value]
        partsResults.append(row)

    partsResults.sort()
    for row in partsResults:
        writer.writerow(row)


with open('data.csv') as f:
    reader = csv.reader(f)
    partsList = list(reader)

partsList.pop(0)

duplicatePart = getDuplicatePart(partsList)
if not (duplicatePart):
    runQuant()
else:
    print("Duplicate found: " + duplicatePart[0])
