from fileutils import writeResults

class SpringPart(object):
    def __init__(self, springPartNumber, springPartQuantityToBuildPod):
        self.springPartNumber = springPartNumber
        self.springPartQuantityToBuildPod = springPartQuantityToBuildPod
        self.toBuy = None

    def setToBuy(self, toBuy):
        self.toBuy = toBuy

    def __lt__(self, other):
        return self.springPartNumber < other.springPartNumber

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

    def getSpringPartBySpringPartNumber(self, springPartNumber):
        for springPart in self.springParts:
            if springPart.springPartNumber == springPartNumber:
                return springPart

    def saveToFile(self):
        path = ('./csv_files/byPart.csv')
        header = ["spring part number", "part quantity for whole pod"]
        rows = []
        for springPart in self.springParts:
            row = [springPart.springPartNumber, springPart.springPartQuantityToBuildPod]
            rows.append(row)
        writeResults(path, header, rows)
