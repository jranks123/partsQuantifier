class Part(object):
    def __init__(self, itemNumber, springPartNumber, itemQuantityToBuildParent, itemQuantityToBuildPod):
        self.itemNumber = itemNumber
        self.springPartNumber = springPartNumber
        self.itemQuantityToBuildParent = itemQuantityToBuildParent
        self.itemQuantityToBuildPod = itemQuantityToBuildPod


def getPart(partItemNumber, partsList):
    for part in partsList:
        if (part.itemNumber == partItemNumber):
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
        if part.itemNumber not in partsDict:
            partsDict[part.itemNumber] = 1
        else:
            return part

def toPartsList(partsListRaw):
    partsList = []
    for rawPart in partsListRaw:
        partObj = {"itemNumber":rawPart[0], "springPartNumber":rawPart[1], "itemQuantityToBuildParent":rawPart[6], "itemQuantityToBuildPod":None}
        part = Part(**partObj)
        partsList.append(part)
    return partsList
