from fileutils import writeResults
from springpart import SpringPartList

class Item(object):
    def __init__(self, itemNumber, springPartNumber, itemQuantityToBuildParent, stock):
        self.itemNumber = self.cleanItemNumber(itemNumber)
        self.springPartNumber = springPartNumber
        self.itemQuantityToBuildParent = itemQuantityToBuildParent
        self.itemQuantityToBuildPod = 0
        self.springPartQuantityToBuildPod = 0
        self.itemNumberParentStockOffset = 0
        self.partNumberParentStockOffset = 0
        self.stockRatio = 0
        self.stockAllocated = 0
        self.stock = int(stock)
        self.parent = None
        self.children = []
        self.stockInParentsPlusStockAllocated = 0


    # Setters
    def setParent(self, parent):
        self.parent = parent

    def setSpringPartQuantityToBuildPod(self, springPartQuantityToBuildPod):
        self.springPartQuantityToBuildPod = springPartQuantityToBuildPod

    def setStockInParentsPlusStockAllocated(self, stockInParentsPlusStockAllocated):
        self.stockInParentsPlusStockAllocated = stockInParentsPlusStockAllocated

    def setItemNumberStockInParentLevelsOnly(self, itemNumberStockInParentLevelsOnly):
        self.itemNumberStockInParentLevelsOnly = itemNumberStockInParentLevelsOnly

    def setNumberOfPodsWorthOfStockInParentLevelsOnly(self, numberOfPodsWorthOfStockInParentLevelsOnly):
        self.numberOfPodsWorthOfStockInParentLevelsOnly = numberOfPodsWorthOfStockInParentLevelsOnly

    def setStockRatio(self, itemQuantityToBuildPod, springPartQuantityToBuildPod):
        self.stockRatio = itemQuantityToBuildPod/springPartQuantityToBuildPod

    def setItemNumberParentStockOffset(self, itemNumberParentStockOffset):
        self.itemNumberParentStockOffset = itemNumberParentStockOffset

    def setPartNumberParentStockOffset(self, partNumberParentStockOffset):
        self.partNumberParentStockOffset = partNumberParentStockOffset

    def setStockAllocated(self, stock, itemNumberParentStockOffset, partNumberParentStockOffset, stockRatio):
        self.stockAllocated = itemNumberParentStockOffset + (stockRatio * (stock - partNumberParentStockOffset))

    def addChild(self, child):
        self.children.append(child)


    def cleanItemNumber(self, itemNumber):
        if itemNumber.endswith(".00"):
            size = len(itemNumber)
            return itemNumber[:size - 3]
        return itemNumber
