class Part(object):
    def __init__(self, itemNumber, springPartNumber, itemQuantityToBuildParent, itemQuantityToBuildPod):
        self.itemNumber = itemNumber
        self.springPartNumber = springPartNumber
        self.itemQuantityToBuildParent = itemQuantityToBuildParent
        self.itemQuantityToBuildPod = itemQuantityToBuildPod

class PartsList(object):
    def __init__(self, partsListRaw):
        partsList = []
        for rawPart in partsListRaw:
            partObj = {"itemNumber":rawPart[0], "springPartNumber":rawPart[1], "itemQuantityToBuildParent":rawPart[6], "itemQuantityToBuildPod":None}
            part = Part(**partObj)
            partsList.append(part)
        self.parts = partsList

    def addPart(self, part):
        parts.append(part)

    def getPart(self, partItemNumber):
        for part in self.parts:
            if (part.itemNumber == partItemNumber):
                return part

    def getParent(self, part):
        if("." not in part):
            return None
        partParts = part.split(".")
        partParts.pop()
        parent = ".".join(partParts)
        return self.getPart(parent)

    def getDuplicatePart(self):
        partsDict = {}
        for part in self.parts:
            if part.itemNumber in partsDict:
                return part
        return None
