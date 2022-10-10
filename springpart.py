from fileutils import writeResults

class SpringPart(object):
    def __init__(self, springPartNumber, springPartQuantityToBuildPod):
        self.springPartNumber = springPartNumber
        self.springPartQuantityToBuildPod = springPartQuantityToBuildPod

class SpringPartList(object):
    def __init__(self, itemList):
        partsDict = {}
        partsResults = []
        for part in itemList.items:
            springPartNumber = part.springPartNumber
            totalQuantity = part.itemQuantityToBuildPod
            if springPartNumber is not None:
                if springPartNumber not in partsDict:
                    partsDict[springPartNumber] = totalQuantity
                else:
                    partsDict[springPartNumber] = partsDict[springPartNumber] + totalQuantity
        for key, value in partsDict.items():
            partsResults.append(SpringPart(key, value))
        partsResults.sort()
        self.springParts = partsResults

    def saveToFile(self):
        path = ('./results/byPart.csv')
        header = ["spring part number", "part quantity for whole pod"]
        rows = []
        for springPart in self.springParts:
            row = [springPart.springPartNumber, springPart.springPartQuantityToBuildPod]
            rows.append(row)
        writeResults(path, header, rows)