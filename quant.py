import csv
from fileutils import writeResults, writeQuantityByPartNumber
from item import Item, ItemList


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
    itemList.saveToFile()
    itemList.springPartsList.saveToFile()
    itemList.calculateStockCollumns(itemList.rootItems)
