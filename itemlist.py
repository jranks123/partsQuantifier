# coding: utf-8
from fileutils import writeResults
from springpart import SpringPartList
from gsheets import push_csv_to_gsheet, find_sheet_id_by_name
from item import Item

class ItemList(object):
    def __init__(self, itemListRaw):
        itemList = []
        for rawItem in itemListRaw:
            if(len(rawItem[1]) > 0):
                itemObj = {"itemNumber":rawItem[0], "springPartNumber":rawItem[1], "itemQuantityToBuildParent":rawItem[2], "stock":rawItem[3], "type": rawItem[4]}
                item = Item(**itemObj)
                itemList.append(item)
            else:
                print("Item " +  rawItem[0] + " has no sprint part number, so it was ignored")
        self.items = itemList
        self.setParents()
        self.setChildren()
        self.setQuantityByItemNumberForAllItems()
        self.springPartsList = SpringPartList(self)
        self.setSpringPartQuantityToBuildPodForAllItems()
        self.setRootItems()
        self.setItemsWithSamePartNumber()


    def getItemByItemNumber(self, itemItemNumber):
        for item in self.items:
            if (item.itemNumber == itemItemNumber):
                return item

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
                    itemsWithSamePartNumber.append(itemToCheck)
                    if len(itemsWithSamePartNumber) > 0:
                        item.setItemsWithSamePartNumber(itemsWithSamePartNumber)

    def partOneCompleteForAllItems(self):
        for item in self.items:
            if item.partOneCompleteForThisItem == False:
                return False
        return True

    def printItemStats(self, itemNumber):
        for item in self.items:
            if item.itemNumber == itemNumber:
                print(" ")
                print("ItemNumber: " + item.itemNumber)
                print("No of pods worth of item number stock in parent levels only: " + str(item.numberOfPodsWorthOfStockInParentLevelsOnly))
                print("Item Number Parent Stock Offest: " + str(item.itemNumberParentStockOffset) if item.setItemNumberParentStockOffset else "N/A")
                print(" ")


    def calculateStockCollumnsPartOne(self, item):
        item.setAllItemsUpToThisPointHaveBeenSolved(True)
        if item.isDuplicateItem() and item.haveSolvedUpToAllOtherItemsWithSameSpringPartNumber() == False:
            item.setItemNumberStockInParentLevelsOnly(item.itemQuantityToBuildParent, item.parent.stockInParentsPlusStockAllocated if item.parent else 0)
            item.setNumberOfPodsWorthOfStockInParentLevelsOnly(item.itemNumberStockInParentLevelsOnly, item.itemQuantityToBuildPod)
            return
        else:
            if item.partOneCompleteForThisItem == False:
                item.setItemNumberStockInParentLevelsOnly(item.itemQuantityToBuildParent, item.parent.stockInParentsPlusStockAllocated if item.parent else 0)
                item.setNumberOfPodsWorthOfStockInParentLevelsOnly(item.itemNumberStockInParentLevelsOnly, item.itemQuantityToBuildPod)
                item.setStockRatio(item.itemQuantityToBuildPod, item.springPartQuantityToBuildPod)
                # we will only get to this line if we have solved for all other duplicates already
                if item.isDuplicateItem():
                    maxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates = item.getMaxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates()
                    # set the item number parent stock offset for this duplicate
                    item.setItemNumberParentStockOffset(maxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates, item.numberOfPodsWorthOfStockInParentLevelsOnly, item.itemQuantityToBuildPod)

                    # we now have to set it for all the other duplicates, as setPartNumberParentStockOffset() needs to know the itemNumberParentStockOffset for all duplicates
                    for duplicateItem in item.itemsWithSamePartNumber:
                        duplicateItem.setItemNumberParentStockOffset(maxNumberOfPodsWorthOfStockInParentLevelsOnlyForDuplicates, duplicateItem.numberOfPodsWorthOfStockInParentLevelsOnly, duplicateItem.itemQuantityToBuildPod)

                    item.setPartNumberParentStockOffset()
                else:
                    item.setItemNumberParentStockOffsetNonDuplicate(0)
                    item.setPartNumberParentStockOffsetNonDuplicate(0)
                item.setStockAllocated(item.stock, item.itemNumberParentStockOffset, item.partNumberParentStockOffset, item.stockRatio)
                item.setStockInParentsPlusStockAllocated(item.stockAllocated, item.itemQuantityToBuildParent, item.parent.stockInParentsPlusStockAllocated if item.parent else 0)
                item.setCanBuildNextLevelUpUsingStockAllocatedForThisItemNumberOnly(item.stockAllocated, item.itemQuantityToBuildParent)
                item.setPartOneCompleteForThisItem(True)
            for child in item.children:
                self.calculateStockCollumnsPartOne(child)


    def calculateStockCollumns(self, rootItems):
        # because of the duplicates, it is possible that we will need to try a couple of times
        count = 1
        while self.partOneCompleteForAllItems() == False:
            for item in rootItems:
                 self.calculateStockCollumnsPartOne(item)
            count+=1


    def calculateCouldHaveOfThisItemNumberIfWeuseAllStockAllocatedInChildrenAndBuildUpToHere(self, item):
        for child in item.children:
            self.calculateCouldHaveOfThisItemNumberIfWeuseAllStockAllocatedInChildrenAndBuildUpToHere(child)
        item.setCouldHaveOfThisItemNumberIfWeuseAllStockAllocatedInChildrenAndBuildUpToHere(item.children, item.stockAllocated)

    def calculateRemainderNeeded(self, item, targetNumberOfPods):
        parentRemainderNeeded = targetNumberOfPods if item.parent is None else item.parent.remainderNeeded
        item.setRemainderNeeded(parentRemainderNeeded, item.itemQuantityToBuildParent, item.stockAllocated)
        for child in item.children:
            self.calculateRemainderNeeded(child, targetNumberOfPods)

    def calculateToBuyPartNumber(self):
        for springPart in self.springPartsList.springParts:
            springPart.setToBuy(0)
            for item in self.items:
                if item.type == "purchased only" or item.type == "assembly/purchased":
                    if item.springPartNumber == springPart.springPartNumber:
                        springPart.setToBuy(springPart.toBuy + item.remainderNeeded if springPart.toBuy is not None else item.remainderNeeded)

        for item in self.items:
            springPart = self.springPartsList.getSpringPartBySpringPartNumber(item.springPartNumber)
            item.setToBuyPartNumber(springPart.toBuy)


    def calculateFinalCollumns(self, rootItems, targetNumberOfPods):
        for item in rootItems:
            self.calculateCouldHaveOfThisItemNumberIfWeuseAllStockAllocatedInChildrenAndBuildUpToHere(item)
            self.calculateRemainderNeeded(item, targetNumberOfPods)
        self.calculateToBuyPartNumber()


    def writeToGsheet(self, API, path, sheetName, SPREADSHEET_ID):
        path = ('./results/' + path)
        push_csv_to_gsheet(
            csv_path=path
            , sheet_id=find_sheet_id_by_name(API, sheetName, SPREADSHEET_ID)
            , SPREADSHEET_ID = SPREADSHEET_ID
            , API = API
        )

    def saveToFile(self, path):
        path = ('./results/' + path)
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
            , 'Could have of this item number if we use all stock allocated in children and build up to here'
            , 'remainder needed'
            , 'To Buy (part number)'

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
                , item.couldHaveOfThisItemNumberIfWeuseAllStockAllocatedInChildrenAndBuildUpToHere
                , item.remainderNeeded
                , item.toBuyPartNumber
                ]
            rows.append(row)
        writeResults(path, header, rows)
