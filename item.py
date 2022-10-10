from fileutils import writeResults

class Item(object):
    def __init__(self, itemNumber, springPartNumber, itemQuantityToBuildParent, itemQuantityToBuildPod):
        self.itemNumber = itemNumber
        self.springPartNumber = springPartNumber
        self.itemQuantityToBuildParent = itemQuantityToBuildParent
        self.itemQuantityToBuildPod = itemQuantityToBuildPod

class ItemList(object):
    def __init__(self, itemListRaw):
        itemList = []
        for rawItem in itemListRaw:
            itemObj = {"itemNumber":rawItem[0], "springPartNumber":rawItem[1], "itemQuantityToBuildParent":rawItem[6], "itemQuantityToBuildPod":None}
            item = Item(**itemObj)
            itemList.append(item)
        self.items = itemList

    def addItem(self, item):
        items.append(item)

    def getItemByItemNumber(self, itemItemNumber):
        for item in self.items:
            if (item.itemNumber == itemItemNumber):
                return item

    def getParentByItemNumber(self, item):
        if("." not in item):
            return None
        itemItems = item.split(".")
        itemItems.pop()
        parentItemNumber = ".".join(itemItems)
        return self.getItemByItemNumber(parentItemNumber)

    def getDuplicateItem(self):
        itemsDict = {}
        for item in self.items:
            if item.itemNumber in itemsDict:
                return item
        return None

    def setQuantityByItemNumber(self):
        for item in self.items:
            accumulatingQuantity = int(item.itemQuantityToBuildParent)
            parentItem = self.getParentByItemNumber(item.itemNumber)
            while(parentItem is not None):
                accumulatingQuantity = accumulatingQuantity * int(parentItem.itemQuantityToBuildParent)
                parentItem = self.getParentByItemNumber(parentItem.itemNumber)
            item.itemQuantityToBuildPod = accumulatingQuantity

    def saveToFile(self):
        path = ('./results/byItemNumber.csv')
        header = ['item number', 'sprint part number', 'item quantity to build parent', 'item quantity for whole pod']
        rows = []
        for item in self.items:
            row = [
                item.itemNumber
                , item.springPartNumber
                , item.itemQuantityToBuildParent
                , item.itemQuantityToBuildPod]
            rows.append(row)
        writeResults(path, header, rows)
