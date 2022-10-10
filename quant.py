import csv
from fileutils import writeResults, writeQuantityByPartNumber
from item import Item, ItemList


def calculateQuantityByPartNumber(itemList):
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
        row = [key, value]
        partsResults.append(row)
    partsResults.sort()
    return partsResults



with open('data.csv') as f:
    reader = csv.reader(f)
    itemListRaw = list(reader)
    f.close()

itemListRaw.pop(0)
itemList = ItemList(itemListRaw)

duplicateItem = itemList.getDuplicateItem()
if (duplicateItem):
    print("Duplicate found: " + duplicateItem.itemNumber)
else:
    itemList.saveItemListToFile()
    quantityByPartNumber = calculateQuantityByPartNumber(itemList)
    writeQuantityByPartNumber(quantityByPartNumber)
