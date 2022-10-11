from fileutils import writeResults
from springpart import SpringPartList

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
        # for item in self.items:
        #     print("item number: " + item.itemNumber)
        #     print("item parent: " + item.parent.itemNumber if item.parent else "No Parent")
        #     print("item children: ")
        #     for child in item.children:
        #         print(child.itemNumber)

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

    def calculateStockCollumns(self, items):
        for item in items:
            if item.parent is None:
                item.setStockInParentsPlusStockAllocated(item.stock)
                item.setItemNumberStockInParentLevelsOnly(0)
                item.setNumberOfPodsWorthOfStockInParentLevelsOnly(0)
            elif len(item.children) > 0:
                for child in item.children:
                    self.calculateStockCollumns(child)


    def saveToFile(self):
        path = ('./results/byItemNumber.csv')
        header = ['item number', 'sprint part number', 'item quantity to build parent', 'item quantity for whole pod', 'spring part quantity to build pod']
        rows = []
        for item in self.items:
            row = [
                item.itemNumber
                , item.springPartNumber
                , item.itemQuantityToBuildParent
                , item.itemQuantityToBuildPod
                , item.springPartQuantityToBuildPod]
            rows.append(row)
        writeResults(path, header, rows)
