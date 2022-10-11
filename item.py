from fileutils import writeResults
from springpart import SpringPartList

class Item(object):
    def __init__(self, itemNumber, springPartNumber, itemQuantityToBuildParent, stock):
        self.itemNumber = self.cleanItemNumber(itemNumber)
        self.springPartNumber = springPartNumber
        self.itemQuantityToBuildParent = int(itemQuantityToBuildParent)
        self.itemQuantityToBuildPod = None
        self.springPartQuantityToBuildPod = None
        self.itemNumberParentStockOffset = None
        self.partNumberParentStockOffset = None
        self.stockRatio = None
        self.stockAllocated = None
        self.canBuildNextLevelUpUsingStockAllocatedForThisItemNumberOnly = None
        self.numberOfPodsWorthOfStockInParentLevelsOnly = None
        self.itemNumberStockInParentLevelsOnly = None
        self.stock = int(stock)
        self.parent = None
        self.children = []
        self.itemsWithSamePartNumber = []
        self.allItemsUpToThisPointHaveBeenSolved = False
        self.partOneCompleteForThisItem = False
        self.stockInParentsPlusStockAllocated = None


    # Setters
    def setParent(self, parent):
        self.parent = parent

    def setAllItemsUpToThisPointHaveBeenSolved(self, allItemsUpToThisPointHaveBeenSolved):
        self.allItemsUpToThisPointHaveBeenSolved = allItemsUpToThisPointHaveBeenSolved

    def setPartOneCompleteForThisItem(self, partOneCompleteForThisItem):
        self.partOneCompleteForThisItem = partOneCompleteForThisItem

    def setSpringPartQuantityToBuildPod(self, springPartQuantityToBuildPod):
        self.springPartQuantityToBuildPod = springPartQuantityToBuildPod

    def setStockInParentsPlusStockAllocated(self, stockAllocated, itemQuantityToBuildParent, parentStockAllocated):
        self.stockInParentsPlusStockAllocated = stockAllocated + (itemQuantityToBuildParent * parentStockAllocated)

    def setItemNumberStockInParentLevelsOnly(self, itemQuantityToBuildParent, stockInParentsPlusStockAllocated):
        self.itemNumberStockInParentLevelsOnly = itemQuantityToBuildParent * stockInParentsPlusStockAllocated

    def setNumberOfPodsWorthOfStockInParentLevelsOnly(self, itemNumberStockInParentLevelsOnly, itemQuantityToBuildPod):
        self.numberOfPodsWorthOfStockInParentLevelsOnly = itemNumberStockInParentLevelsOnly/itemQuantityToBuildPod

    def setStockRatio(self, itemQuantityToBuildPod, springPartQuantityToBuildPod):
        self.stockRatio = itemQuantityToBuildPod/float(springPartQuantityToBuildPod)

    def setItemNumberParentStockOffset(self, maxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates, numberOfPodsWorthOfStockInParentLevelsOnly, itemQuantityToBuildPod):
        self.itemNumberParentStockOffset = (maxNumberOfPodsWorthOfStockInParentLevelsOnlyBetweenItemsWithSamePartNumber - numberOfPodsWorthOfStockInParentLevelsOnly) * itemQuantityToBuildPod

    def setItemNumberParentStockOffsetNonDuplicate(self, itemNumberParentStockOffset):
        self.itemNumberParentStockOffset = itemNumberParentStockOffset

    def setPartNumberParentStockOffset(self):
        currentTotal = self.itemNumberParentStockOffset
        for item in self.itemsWithSamePartNumber:
            currentTotal += item.itemNumberParentStockOffset
        self.partNumberParentStockOffset = currentTotal

    def setPartNumberParentStockOffsetNonDuplicate(self, partNumberParentStockOffset):
        self.partNumberParentStockOffset = partNumberParentStockOffset

    def setStockAllocated(self, stock, itemNumberParentStockOffset, partNumberParentStockOffset, stockRatio):
        self.stockAllocated = itemNumberParentStockOffset + (stockRatio * (stock - partNumberParentStockOffset))

    def setCanBuildNextLevelUpUsingStockAllocatedForThisItemNumberOnly(self, stockRatio, stockAllocated):
        self.canBuildNextLevelUpUsingStockAllocatedForThisItemNumberOnly = stockAllocated/stockRatio


    def setItemsWithSamePartNumber(self, items):
        self.itemsWithSamePartNumber = items

    def addChild(self, child):
        self.children.append(child)

    def getMaxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates(self):
        currentMax = self.numberOfPodsWorthOfStockInParentLevelsOnly
        for item in self.itemsWithSamePartNumber:
            if item.numberOfPodsWorthOfStockInParentLevelsOnly > currentMax:
                currentMax = item.numberOfPodsWorthOfStockInParentLevelsOnly
        return currentMax

    def getChildrenString(self):
        childString = ""
        for child in self.children:
            childString += (child.itemNumber + " ")
        return childString

    def haveSolvedUpToAllOtherItemsWithSameSpringPartNumber(self):
        for item in self.itemsWithSamePartNumber:
            if item.allItemsUpToThisPointHaveBeenSolved == False:
                return False
        return True

    def isDuplicateItem(self):
        return len(self.itemsWithSamePartNumber) > 0

    def cleanItemNumber(self, itemNumber):
        if itemNumber.endswith(".00"):
            size = len(itemNumber)
            return itemNumber[:size - 3]
        return itemNumber
