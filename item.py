from fileutils import writeResults

class Item(object):
    def __init__(self, itemNumber, springPartNumber, itemQuantityToBuildParent, stock):
        self.itemNumber = self.cleanItemNumber(itemNumber)
        self.springPartNumber = springPartNumber
        self.itemQuantityToBuildParent = itemQuantityToBuildParent
        self.itemQuantityToBuildPod = None
        self.stock = stock
        self.parent = None
        self.children = []

    def setParent(self, parent):
        self.parent = parent

    def addChild(self, child):
        self.children.append(child)

    def getParent(self):
        return self.parent

    def cleanItemNumber(self, itemNumber):
        if itemNumber.endswith(".00"):
            size = len(itemNumber)
            return itemNumber[:size - 3]
        return itemNumber


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
        for item in self.items:
            print("item number: " + item.itemNumber)
            print("item parent: " + item.parent.itemNumber if item.parent else "No Parent")
            print("item children: ")
            for child in item.children:
                print(child.itemNumber)

    def getItemByItemNumber(self, itemItemNumber):
        for item in self.items:
            if (item.itemNumber == itemItemNumber):
                return item

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

    def setQuantityByItemNumber(self):
        for item in self.items:
            accumulatingQuantity = int(item.itemQuantityToBuildParent)
            parentItem = item.parent
            while(parentItem is not None):
                accumulatingQuantity = accumulatingQuantity * int(parentItem.itemQuantityToBuildParent)
                parentItem = parentItem.parent
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
