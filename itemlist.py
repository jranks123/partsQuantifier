from fileutils import writeResults
from springpart import SpringPartList
from item import Item

class ItemList(object):
    def __init__(self, itemListRaw):
        itemList = []
        for rawItem in itemListRaw:
            itemObj = {"itemNumber":rawItem[0], "springPartNumber":rawItem[1], "itemQuantityToBuildParent":rawItem[2], "stock":rawItem[3]}
            item = Item(**itemObj)
            itemList.append(item)
        self.items = itemList
        self.setParents()
        self.setChildren()
        self.setQuantityByItemNumberForAllItems()
        self.createSpringPartList()
        self.setSpringPartQuantityToBuildPodForAllItems()
        self.setRootItems()


    def getItemByItemNumber(self, itemItemNumber):
        for item in self.items:
            if (item.itemNumber == itemItemNumber):
                return item

    def createSpringPartList(self):
        self.springPartsList = SpringPartList(self)

    def setSpringPartQuantityToBuildPodForAllItems(self):
        for item in self.items:
            for springPart in self.springPartsList.springParts:
                if item.springPartNumber == springPart.springPartNumber:
                    item.springPartQuantityToBuildPod = springPart.springPartQuantityToBuildPod

    def setParents(self):
        for item in self.items:
            if("." in item.itemNumber):
                itemNumberParts = item.itemNumber.split(".")
                itemNumberParts.pop()
                parentItemNumber = ".".join(itemNumberParts)
                item.setParent(self.getItemByItemNumber(parentItemNumber))


    def setChildren(self):
        for i in self.items:
            for j in self.items:
                if i.parent and i.parent.itemNumber == j.itemNumber:
                    j.addChild(i)

    def getDuplicateItem(self):
        itemsDict = {}
        for item in self.items:
            if item.itemNumber in itemsDict:
                return item
        return None

    def setQuantityByItemNumberForAllItems(self):
        for item in self.items:
            accumulatingQuantity = int(item.itemQuantityToBuildParent)
            parentItem = item.parent
            while(parentItem is not None):
                accumulatingQuantity = accumulatingQuantity * int(parentItem.itemQuantityToBuildParent)
                parentItem = parentItem.parent
            item.itemQuantityToBuildPod = accumulatingQuantity

    def setRootItems(self):
        rootItems = []
        for item in self.items:
            if item.parent is None:
                rootItems.append(item)
        self.rootItems = rootItems


    def setItemsWithSamePartNumber(self):
        for itemToCheck in self.items:
            itemsWithSamePartNumber = []
            for item in self.items:
                if item.springPartNumber == itemToCheck.springPartNumber and item.itemNumber != itemToCheck.itemNumber:
                    itemsWithSamePartNumber.append(item)
                item.setItemsWithSamePartNumber(itemsWithSamePartNumber)

    def partOneCompleteForAllItems(self):
        for item in self.items:
            if item.partOneCompleteForThisItem == False:
                return False
        return True

    def calculateStockCollumnsPartOneForItem(self, item):
        item.setAllItemsUpToThisPointHaveBeenSolved(True)
        if item.isDuplicateItem() and item.haveSolvedUpToAllOtherItemsWithSameSpringPartNumber() == False:
            # do nothing
            return
        else:
            if item.partOneCompleteForThisItem == False:
                item.setItemNumberStockInParentLevelsOnly(item.itemQuantityToBuildParent, item.parent.stockInParentsPlusStockAllocated if item.parent else 0)
                item.setNumberOfPodsWorthOfStockInParentLevelsOnly(item.itemNumberStockInParentLevelsOnly, item.itemQuantityToBuildPod)
                item.setStockRatio(item.itemQuantityToBuildPod, item.springPartQuantityToBuildPod)
                maxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates = item.getMaxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates()
                if item.isDuplicateItem():
                    item.setItemNumberParentStockOffset(maxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates, item.numberOfPodsWorthOfStockInParentLevelsOnly, item.itemQuantityToBuildPod)
                    item.setPartNumberParentStockOffset()
                else:
                    item.setItemNumberParentStockOffsetNonDuplicate(0)
                    item.setPartNumberParentStockOffsetNonDuplicate(0)
                item.setStockAllocated(item.stock, item.itemNumberParentStockOffset, item.partNumberParentStockOffset, item.stockRatio)
                item.setStockInParentsPlusStockAllocated(item.stockAllocated, item.itemQuantityToBuildParent, item.parent.stockAllocated if item.parent else 0)
                item.setPartOneCompleteForThisItem(True)
            for child in item.children:
                self.calculateStockCollumnsPartOneForItem(child)


    def calculateStockCollumnsPartOne(self, rootItems):
        # because of the duplicates, it is likely that we will need to try a couple of times
        while self.partOneCompleteForAllItems() == False:
            for item in rootItems:
                 self.calculateStockCollumnsPartOneForItem(item)

    def calculateStockCollumnsPartTwo(self, items):

        for item in items:
            if item.parent is not None:
                item.setItemNumberParentStockOffset(item.maxNumberOfPodsWorthOfStockInParentLevelsOnlyBetweenItemsWithSamePartNumber, item.numberOfPodsWorthOfStockInParentLevelsOnly, item.itemQuantityToBuildPod)
                self.calculateStockCollumnsPartTwo(item.children)




    def saveToFile(self):
        path = ('./results/byItemNumber.csv')
        header = [
            'item number'
            , 'item parent'
            , 'item children'
            , 'sprint part number'
            , 'item quantity to build parent'
            , 'item quantity for whole pod'
            , 'spring part quantity to build pod'
            , 'stock'
            , 'stock In Parents Plus Stock Allocated'
            , 'Item Number Stock In Parent Levels Only'
            , 'Number Of Pods Worth Of Stock In Parent Levels Only'
            , 'Item number parent stock offset'
            , 'Part Number Parent Stock Offset'
            , 'stock ratio'
            , 'stock allocated'
            , 'Can build next level up using stock allocated for this item number only'

        ]
        rows = []
        for item in self.items:
            row = [
                item.itemNumber
                , item.parent.itemNumber if item.parent else "N/A"
                , item.getChildrenString()
                , item.springPartNumber
                , item.itemQuantityToBuildParent
                , item.itemQuantityToBuildPod
                , item.springPartQuantityToBuildPod
                , item.stock
                , item.stockInParentsPlusStockAllocated
                , item.itemNumberStockInParentLevelsOnly
                , item.numberOfPodsWorthOfStockInParentLevelsOnly
                , item.itemNumberParentStockOffset
                , item.partNumberParentStockOffset
                , item.stockRatio
                , item.stockAllocated
                , item.canBuildNextLevelUpUsingStockAllocatedForThisItemNumberOnly    
                ]
            rows.append(row)
        writeResults(path, header, rows)
